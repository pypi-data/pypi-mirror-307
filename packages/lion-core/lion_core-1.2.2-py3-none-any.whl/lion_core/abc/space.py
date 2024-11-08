from abc import abstractmethod
from collections.abc import Iterable
from typing import Any, Generic, TypeVar

from .characteristic import Traversal
from .concept import AbstractElement, AbstractSpace

T = TypeVar("T")


class Container(AbstractSpace, AbstractElement, Generic[T]):
    """Container for items."""

    @abstractmethod
    def __contains__(self, item: object) -> bool:
        """Check if an item is in the space."""


class Ordering(Container, Generic[T]):
    """Container with a defined order. Subclass must have order attribute."""

    order: list[T]


class Collective(Container, Generic[T]):
    """Container representing a collection of items."""

    @abstractmethod
    def items(self) -> Iterable[tuple[Any, T]]:
        """
        Get the items in the collective.

        Returns:
            Iterable: The items in the collective.
        """

    @abstractmethod
    def values(self) -> Iterable[T]:
        """
        Get the values in the collective.

        Returns:
            Iterable: The values in the collective.
        """

    @abstractmethod
    def keys(self) -> Iterable[Any]:
        """
        Get the keys in the collective.

        Returns:
            Iterable: The keys in the collective.
        """


class Structure(Container, Traversal, Generic[T]):
    """Traversable container structure"""


__all__ = ["Container", "Ordering", "Collective", "Structure"]
