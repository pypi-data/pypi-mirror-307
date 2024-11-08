import logging
from collections.abc import Callable
from pathlib import Path
from typing import Literal

import pandas as pd
from lion_service import iModel
from lionfuncs import alcall
from pydantic import model_validator

from lion_core.action import Tool, ToolManager
from lion_core.communication import (
    MESSAGE_FIELDS,
    ActionRequest,
    ActionResponse,
    AssistantResponse,
    Instruction,
    MessageManager,
)
from lion_core.generic import LogManager, Node, Pile, Progression
from lion_core.protocols.operatives import ActionResponseModel, Operative, Step
from lion_core.settings import Settings
from lion_core.types import BaseModel, FieldModel, NewModelParams


class Branch(Node):

    user: str | None = None
    name: str | None = None
    msgs: MessageManager = None
    tool_manager: ToolManager = None
    imodel: iModel | None = None
    parse_imodel: iModel | None = None

    @model_validator(mode="before")
    def _validate_data(cls, data: dict) -> dict:

        user = data.pop("user", None)
        name = data.pop("name", None)
        message_manager = data.pop("msgs", None)
        if not message_manager:
            message_manager = MessageManager(
                messages=data.pop("messages", None),
                logger=data.pop("logger", None),
                system=data.pop("system", None),
            )
        if not message_manager.logger:
            message_manager.logger = LogManager(
                **Settings.Branch.BRANCH.message_log_config.clean_dump()
            )

        tool_manager = data.pop("tool_manager", None)
        if not tool_manager:
            tool_manager = ToolManager()
            tool_manager.logger = LogManager(
                **Settings.Branch.BRANCH.action_log_config.clean_dump()
            )
        if "tools" in data:
            data["tool_manager"].register_tools(data.pop("tools"))

        imodel = data.pop(
            "imodel",
            iModel(**Settings.iModel.CHAT.clean_dump()),
        )
        out = {
            "user": user,
            "name": name,
            "msgs": message_manager,
            "tool_manager": tool_manager,
            "imodel": imodel,
            **data,
        }
        return out

    async def invoke_action(
        self,
        action_request: ActionRequest | BaseModel | dict,
        suppress_errors: bool = False,
    ) -> ActionResponse:
        try:
            func, args = None, None
            if isinstance(action_request, BaseModel):
                if hasattr(action_request, "function") and hasattr(
                    action_request, "arguments"
                ):
                    func = action_request.function
                    args = action_request.arguments
            elif isinstance(action_request, dict):
                if action_request.keys() >= {"function", "arguments"}:
                    func = action_request["function"]
                    args = action_request["arguments"]

            result = await self.tool_manager.invoke(action_request)
            tool = self.tool_manager.registry[action_request.function]

            if not isinstance(action_request, ActionRequest):
                action_request = await self.msgs.a_add_message(
                    function=func,
                    arguments=args,
                    sender=self,
                    recipient=tool,
                )

            await self.msgs.a_add_message(
                action_request=action_request,
                action_response=result,
            )

            return ActionResponseModel(
                function=action_request.function,
                arguments=action_request.arguments,
                output=result,
            )
        except Exception as e:
            if suppress_errors:
                logging.error(f"Error invoking action: {e}")
            else:
                raise e

    def get_tool_schema(
        self,
        tools: str | Tool | list[Tool | str] | bool,
        auto_register: bool = True,
    ) -> dict:
        tools = tools if isinstance(tools, list) else [tools]
        if auto_register:
            for i in tools:
                if (
                    isinstance(i, Tool | Callable)
                    and i not in self.tool_manager
                ):
                    self.tool_manager.register_tools(i)
        return self.tool_manager.get_tool_schema(tools)

    def dump_log(self, clear: bool = True, persist_path: str | Path = None):
        self.msgs.logger.dump(clear, persist_path)
        self.tool_manager.logger.dump(clear, persist_path)

    def to_df(self, *, progress: Progression = None) -> pd.DataFrame:
        if progress is None:
            progress = self.msgs.progress

        msgs = [
            self.msgs.messages[i] for i in progress if i in self.msgs.messages
        ]
        p = Pile(items=msgs)
        return p.to_df(columns=MESSAGE_FIELDS)

    async def operate(
        self,
        *,
        instruction=None,
        guidance=None,
        context=None,
        sender=None,
        recipient=None,
        operative_model: type[BaseModel] = None,
        progress=None,
        imodel: iModel = None,
        reason: bool = False,
        actions: bool = False,
        exclude_fields: list | dict | None = None,
        handle_validation: Literal[
            "raise", "return_value", "return_none"
        ] = "return_value",
        invoke_actions: bool = True,
        tool_schemas=None,
        images: list = None,
        image_detail: Literal["low", "high", "auto"] = None,
        max_retries: int = None,
        retry_imodel: iModel = None,
        retry_kwargs: dict = {},
        auto_retry_parse: bool = True,
        field_models: list[FieldModel] | None = None,
        skip_validation: bool = False,
        tools: str | Tool | list[Tool | str] | bool = None,
        request_params: NewModelParams = None,
        request_param_kwargs: dict = {},
        response_params: NewModelParams = None,
        response_param_kwargs: dict = {},
        **kwargs,
    ) -> BaseModel | None | dict | str:
        imodel = imodel or self.imodel
        retry_imodel = retry_imodel or imodel

        operative: Operative = Step.request_operative(
            request_params=request_params,
            reason=reason,
            actions=actions,
            exclude_fields=exclude_fields,
            base_type=operative_model,
            field_models=field_models,
            **request_param_kwargs,
        )
        if isinstance(max_retries, int) and max_retries > 0:
            operative.max_retries = max_retries

        if auto_retry_parse is True:
            operative.auto_retry_parse = True

        if invoke_actions and tools:
            tool_schemas = self.get_tool_schema(tools)

        ins, res = await self._invoke_imodel(
            instruction=instruction,
            guidance=guidance,
            context=context,
            sender=sender,
            recipient=recipient,
            request_model=operative.request_type,
            progress=progress,
            imodel=imodel,
            images=images,
            image_detail=image_detail,
            tool_schemas=tool_schemas,
            **kwargs,
        )
        self.msgs.add_message(instruction=ins)
        self.msgs.add_message(assistant_response=res)

        operative.response_str_dict = res.response
        if skip_validation:
            return operative.response_str_dict

        response_model = operative.update_response_model(res.response)
        max_retries = operative.max_retries

        num_try = 0
        parse_imodel = self.parse_imodel or imodel or self.imodel
        while (
            operative._should_retry
            and isinstance(response_model, str | dict)
            and num_try < max_retries
        ):
            num_try += 1
            if operative.auto_retry_parse:
                instruct = Instruction(
                    instruction="reformat text into specified model",
                    guidance="follow the required response format, using the model schema as a guide",
                    context=[{"text_to_format": res.response}],
                    request_model=operative.request_type,
                    sender=self.user,
                    recipient=self,
                )

            api_request = parse_imodel.parse_to_data_model(
                messages=[instruct.chat_msg], **(retry_kwargs or {})
            )
            res1 = AssistantResponse(
                sender=self,
                recipient=self.user,
                assistant_response=await parse_imodel.invoke(**api_request),
            )
            response_model = operative.update_response_model(res1.response)

        if isinstance(response_model, dict | str):
            if handle_validation == "raise":
                raise ValueError(
                    "Operative model validation failed. iModel response"
                    " not parsed into operative model:"
                    f" {operative.name}"
                )
            if handle_validation == "return_none":
                return None
            if handle_validation == "return_value":
                return response_model

        if (
            invoke_actions is True
            and getattr(response_model, "action_required", None) is True
            and getattr(response_model, "action_requests", None) is not None
        ):
            action_response_models = await alcall(
                response_model.action_requests,
                self.invoke_action,
                suppress_errors=True,
            )
            action_response_models = [
                i.model_dump() for i in action_response_models if i
            ]
            operative = Step.respond_operative(
                response_params=response_params,
                operative=operative,
                additional_data={"action_responses": action_response_models},
                **response_param_kwargs,
            )
            response_model = operative.response_model
        elif (
            hasattr(response_model, "action_requests")
            and response_model.action_requests
        ):
            for i in response_model.action_requests:
                act_req = ActionRequest(
                    function=i.function,
                    arguments=i.arguments,
                    sender=self,
                )
                self.msgs.add_message(
                    action_request=act_req,
                    sender=act_req.sender,
                    recipient=None,
                )

        return operative.response_model

    async def _invoke_imodel(
        self,
        instruction=None,
        guidance=None,
        context=None,
        sender=None,
        recipient=None,
        request_fields=None,
        request_model: type[BaseModel] = None,
        progress=None,
        imodel: iModel = None,
        tool_schemas=None,
        images: list = None,
        image_detail: Literal["low", "high", "auto"] = None,
        **kwargs,
    ) -> tuple[Instruction, AssistantResponse]:

        ins = self.msgs.create_instruction(
            instruction=instruction,
            guidance=guidance,
            context=context,
            sender=sender or self.user or "user",
            recipient=recipient or self.ln_id,
            request_model=request_model,
            request_fields=request_fields,
            images=images,
            image_detail=image_detail,
            tool_schemas=tool_schemas,
        )
        kwargs["messages"] = self.msgs.to_chat_msgs(progress)
        kwargs["messages"].append(ins.chat_msg)

        imodel = imodel or self.imodel
        api_request = imodel.parse_to_data_model(**kwargs)
        api_response = await imodel.invoke(**api_request)
        res = AssistantResponse(
            assistant_response=api_response,
            sender=self,
            recipient=self.user,
        )
        return ins, res
