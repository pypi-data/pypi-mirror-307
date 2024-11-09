from collections.abc import Iterator
from typing import Any

from typing_extensions import override

from lion_core.abc import BaseExecutor, EventStatus
from lion_core.generic import Pile, Progression
from lion_core.types import ID

from .action_processor import ActionProcessor
from .base import ObservableAction


class ActionExecutor(BaseExecutor):
    """
    Executor class for managing and processing actions.

    This class is responsible for managing a collection of actions, tracking
    their status, and processing them using a specified processor class.

    Attributes:
        processor_config (dict): Configuration for initializing the processor.
        processor_class (Type[ActionProcessor]): Class used to process actions.
        pile (Pile): A collection of actions managed by the executor.
        pending (Progression): A progression tracking the pending actions.
    """

    processor_class: type[ActionProcessor] = ActionProcessor
    strict: bool = True

    @override
    def __init__(self, **kwargs: Any) -> None:
        """
        Initializes the ActionExecutor with the provided configuration.

        Args:
            **kwargs: Configuration parameters for initializing the processor.
        """
        super().__init__(**kwargs)
        self.pile: Pile[ObservableAction] = Pile(
            item_type={self.processor_class.event_type},
            strict_type=self.strict,
        )
        self.pending: Progression = Progression()
        self.processor: ActionProcessor = None

    @property
    def pending_action(self) -> Pile[ObservableAction]:
        """
        Retrieves a pile of all pending actions.

        Returns:
            Pile: A collection of actions that are still pending.
        """
        return Pile(
            items=[i for i in self.pile if i.status == EventStatus.PENDING],
        )

    @property
    def completed_action(self) -> Pile[ObservableAction]:
        """
        Retrieves a pile of all completed actions.

        Returns:
            Pile: A collection of actions that have been completed.
        """
        return Pile(
            items=[i for i in self.pile if i.status == EventStatus.COMPLETED],
        )

    async def append(self, action: ID[ObservableAction].Item) -> None:
        """
        Appends a new action to the executor.

        Args:
            action (ObservableAction): The action to be added to the pile.
        """
        async with self.pile:
            self.pile.include(item=action)
            self.pending.include(item=action)

    @override
    async def forward(self) -> None:
        """Forwards pending actions to the processor."""
        while len(self.pending) > 0:
            action = self.pile[self.pending.popleft()]
            await self.processor.enqueue(action)
        await self.processor.process()

    def __contains__(self, action: ID[ObservableAction].Ref) -> bool:
        """Checks if an action is present in the pile."""
        return action in self.pile

    def __iter__(self) -> Iterator[ObservableAction]:
        """Returns an iterator over the actions in the pile."""
        return iter(self.pile)


__all__ = ["ActionExecutor"]
# File: lion_core/action/action_executor.py
