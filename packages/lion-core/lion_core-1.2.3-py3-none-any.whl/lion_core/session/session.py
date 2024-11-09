from collections.abc import Callable

import pandas as pd
from lion_service import iModel
from lionfuncs import to_list

from lion_core.action import Tool, ToolManager
from lion_core.communication import (
    MESSAGE_FIELDS,
    MailManager,
    RoledMessage,
    System,
)
from lion_core.exceptions import ItemNotFoundError, LionValueError
from lion_core.generic import Exchange, Node, Pile, Progression, to_list_type
from lion_core.types import ID, Field, JsonValue

from .branch import Branch


class Session(Node):
    """
    Manages multiple conversation branches and mail transfer in a session.

    Attributes:
        branches (Pile | None): Collection of conversation branches.
        default_branch (Branch | None): The default conversation branch.
        mail_transfer (Exchange | None): Mail transfer system.
        mail_manager (MailManager | None): Manages mail operations.
    """

    branches: Pile = Field(default_factory=Pile)
    default_branch: Branch = Field(default_factory=Branch, exclude=True)
    mail_transfer: Exchange = Field(default_factory=Exchange)
    mail_manager: MailManager = Field(
        default_factory=MailManager, exclude=True
    )

    def new_branch(
        self,
        system: System | JsonValue = None,
        system_sender: ID.SenderRecipient = None,
        system_datetime: bool | str = None,
        user: ID.SenderRecipient = None,
        name: str | None = None,
        imodel: iModel = None,
        messages: Pile[RoledMessage] = None,
        progress: Progression = None,
        tool_manager: ToolManager = None,
        tools: Tool | Callable | list = None,
        **kwargs,  # additional branch parameters
    ) -> Branch:

        kwargs["system"] = system
        kwargs["system_sender"] = system_sender
        kwargs["system_datetime"] = system_datetime
        kwargs["user"] = user
        kwargs["name"] = name
        kwargs["imodel"] = imodel
        kwargs["messages"] = messages
        kwargs["progress"] = progress
        kwargs["tool_manager"] = tool_manager
        kwargs["tools"] = tools
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        branch = Branch(**kwargs)

        self.branches.include(branch)
        self.mail_manager.add_sources(branch)
        if self.default_branch is None:
            self.default_branch = branch
        return branch

    def remove_branch(
        self,
        branch: ID.Ref,
        delete: bool = False,
    ):
        branch = ID.get_id(branch)

        if branch not in self.branches:
            _s = (
                str(branch)
                if len(str(branch)) < 10
                else str(branch)[:10] + "..."
            )
            raise ItemNotFoundError(f"Branch {_s}.. does not exist.")
        branch: Branch = self.branches[branch]

        self.branches.exclude(branch)
        self.mail_manager.delete_source(branch.ln_id)

        if self.default_branch.ln_id == branch.ln_id:
            if self.branches.is_empty():
                self.default_branch = None
            else:
                self.default_branch = self.branches[0]

        if delete:
            del branch

    async def asplit(self, branch: ID.Ref) -> Branch:
        """
        Split a branch, creating a new branch with the same messages and tools.

        Args:
            branch: The branch to split or its identifier.

        Returns:
            The newly created branch.
        """
        async with self.branches:
            return self.split(branch)

    def split(self, branch: ID.Ref) -> Branch:
        """
        Split a branch, creating a new branch with the same messages and tools.

        Args:
            branch: The branch to split or its identifier.

        Returns:
            The newly created branch.
        """
        branch: Branch = self.branches[branch]
        branch_clone = branch.clone(sender=self.ln_id)
        self.branches.append(branch_clone)
        self.mail_manager.add_sources(branch_clone)
        return branch_clone

    def change_default_branch(self, branch: ID.Ref):
        """
        Change the default branch of the session.

        Args:
            branch: The branch to set as default or its identifier.
        """
        branch = self.branches[branch]
        if branch and len(branch) == 1:
            self.default_branch = branch
        raise LionValueError("Session can only have one default branch.")

    def collect(self, from_: ID.RefSeq = None):
        """
        Collect mail from specified branches.

        Args:
            from_: The branches to collect mail from. If None, collect
                from all.

        Raises:
            ValueError: If mail collection fails.
        """
        if from_ is None:
            self.mail_manager.collect_all()
        else:
            try:
                sources = to_list_type(from_)
                for source in sources:
                    self.mail_manager.collect(ID.get_id(source))
            except Exception as e:
                raise ValueError(f"Failed to collect mail. Error: {e}")

    def send(self, to_: ID.RefSeq = None):
        """
        Send mail to specified branches.

        Args:
            to_: The branches to send mail to. If None, send to all.

        Raises:
            ValueError: If mail sending fails.
        """
        if to_ is None:
            self.mail_manager.send_all()
        else:
            try:
                sources = to_list_type(to_)
                for source in sources:
                    self.mail_manager.send(ID.get_id(source))
            except Exception as e:
                raise ValueError(f"Failed to send mail. Error: {e}")

    def collect_send_all(self, receive_all: bool = False):
        """
        Collect and send mail for all branches, optionally receiving all mail.

        Args:
            receive_all: If True, receive all mail for all branches.
        """
        self.collect()
        self.send()
        if receive_all:
            for branch in self.branches:
                branch.receive_all()

    def to_df(self, branches: ID.RefSeq = None) -> pd.DataFrame:
        out = self.concat_messages(branches=branches)
        return out.to_df(columns=MESSAGE_FIELDS)

    def concat_messages(
        self, branches: ID.RefSeq = None
    ) -> Pile[RoledMessage]:
        if not branches:
            branches = self.branches
        if isinstance(branches, dict):
            branches = to_list(branches, use_values=True)

        out = Pile(item_type={RoledMessage})
        for i in branches:
            if i not in self.branches:
                _msg = str(i)
                _msg = _msg[:50] if len(_msg) > 50 else _msg
                raise ItemNotFoundError(
                    f"Branch <{_msg}> was not found in the session."
                )

            b: Branch = self.branches[i]
            out |= b.msgs.messages

        return out


__all__ = ["Session"]
# File: lion_core/session/session.py
