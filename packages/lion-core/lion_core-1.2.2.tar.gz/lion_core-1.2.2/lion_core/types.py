from collections.abc import Mapping, Sequence
from typing import Annotated, Generic, Literal, TypeAlias, TypeVar

from lionfuncs import (
    LN_UNDEFINED,
    LionUndefinedType,
    insert_random_hyphens,
    unique_hash,
)
from pydantic import BaseModel, ConfigDict, Field, JsonValue, PrivateAttr
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from lion_core.abc import Container, Observable, Ordering
from lion_core.exceptions import LionIDError
from lion_core.settings import LionIDConfig, Settings

from .models import (
    BaseLionModel,
    FieldModel,
    NewModelParams,
    Note,
    OperableModel,
    SchemaModel,
)

INDICE_TYPE = str | list[str | int]
FIELD_NAME = TypeVar("FIELD_NAME", bound=str)

T = TypeVar("T", bound=Observable)
LnID: TypeAlias = Annotated[str, Field(description="Lion ID string ('ln...')")]


class ID(Generic[T]):
    """
    Generic type definitions for different ID usage contexts.

    TypeVars:
        T: Type parameter constrained to Observable types
    """

    # For functions that accept either ID or item
    Ref: TypeAlias = LnID | T  # type: ignore

    # For functions requiring just the ID
    ID: TypeAlias = LnID

    # For functions requiring Observable object
    Item = T  # type: ignore

    # For collections
    IDSeq: TypeAlias = Sequence[LnID] | Ordering[LnID]
    ItemSeq: TypeAlias = (  # type: ignore
        Sequence[T] | Mapping[LnID, T] | Container[LnID | T]
    )
    RefSeq: TypeAlias = IDSeq | ItemSeq

    # For system-level interactions
    SenderRecipient: TypeAlias = (  # type: ignore
        LnID | T | Literal["system", "user", "N/A", "assistant"]
    )

    @staticmethod
    def id(
        config: LionIDConfig = Settings.Config.ID,
        n: int = None,
        prefix: str = None,
        postfix: str = None,
        random_hyphen: bool = None,
        num_hyphens: int = None,
        hyphen_start_index: int = None,
        hyphen_end_index: int = None,
    ) -> LnID:
        """
        Generate a unique identifier.

        Args:
            n: Length of the ID (excluding prefix and postfix).
            prefix: String to prepend to the ID.
            postfix: String to append to the ID.
            random_hyphen: If True, insert random hyphens into the ID.
            num_hyphens: Number of hyphens to insert if random_hyphen is True.
            hyphen_start_index: Start index for hyphen insertion.
            hyphen_end_index: End index for hyphen insertion.

        Returns:
            A unique identifier string.
        """
        _dict = {
            "n": n,
            "prefix": prefix,
            "postfix": postfix,
            "random_hyphen": random_hyphen,
            "num_hyphens": num_hyphens,
            "hyphen_start_index": hyphen_start_index,
            "hyphen_end_index": hyphen_end_index,
        }
        _dict = {k: v for k, v in _dict.items() if v is not None}
        config = {**config.clean_dump(), **_dict}
        return ID._id(**config)

    @staticmethod
    def _id(
        *,
        n: int,
        prefix: str = "",
        postfix: str = "",
        random_hyphen: bool = False,
        num_hyphens: int = 0,
        hyphen_start_index: int = 6,
        hyphen_end_index: int = -6,
    ):
        _id = unique_hash(n)
        if random_hyphen:
            _id = insert_random_hyphens(
                s=_id,
                num_hyphens=num_hyphens,
                start_index=hyphen_start_index,
                end_index=hyphen_end_index,
            )
        if prefix:
            _id = f"{prefix}{_id}"
        if postfix:
            _id = f"{_id}{postfix}"

        return _id

    @staticmethod
    def get_id(
        item,
        config: LionIDConfig = Settings.Config.ID,
        /,
    ) -> str:
        """
        Get the Lion ID of an item.

        Args:
            item: The item to get the ID from.
            config: Configuration dictionary for ID validation.

        Returns:
            The Lion ID of the item.

        Raises:
            LionIDError: If the item does not contain a valid Lion ID.
        """

        item_id = None
        if isinstance(item, Sequence) and len(item) == 1:
            item = item[0]

        if isinstance(item, Observable):
            item_id: str = item.ln_id
        else:
            item_id = item

        check = isinstance(item_id, str)
        if check:
            id_len = (
                (len(config.prefix) if config.prefix else 0)
                + config.n
                + config.num_hyphens
                + (len(config.postfix) if config.postfix else 0)
            )
            if len(item_id) != id_len:
                check = False
        if check and config.prefix:
            if item_id.startswith(config.prefix):
                item_id = item_id[len(config.prefix) :]  # noqa
            else:
                check = False
        if check and config.postfix:
            if item_id.endswith(config.postfix):
                item_id = item_id[: -len(config.postfix)]
            else:
                check = False
        if check and config.num_hyphens:
            if config.num_hyphens != item_id.count("-"):
                check = False
        if check and config.hyphen_start_index:
            idx = config.hyphen_start_index - len(config.prefix)
            if idx > 0 and "-" in item_id[:idx]:
                check = False
        if check and config.hyphen_end_index:
            if config.hyphen_end_index < 0:
                idx = config.hyphen_end_index + id_len
            idx -= len(config.prefix + config.postfix)
            if idx < 0 and "-" in item_id[idx:]:
                check = False

        if check:
            return config.prefix + item_id + config.postfix
        if (
            isinstance(item_id, str) and len(item_id) == 32
        ):  # for backward compatibility
            return item_id
        raise LionIDError(
            f"The input object of type <{type(item).__name__}> does "
            "not contain or is not a valid Lion ID. Item must be an instance"
            " of `Observable` or a valid `ln_id`."
        )

    @staticmethod
    def is_id(
        item,
        config: LionIDConfig = Settings.Config.ID,
        /,
    ) -> bool:
        """
        Check if an item is a valid Lion ID.

        Args:
            item: The item to check.
            config: Configuration dictionary for ID validation.

        Returns:
            True if the item is a valid Lion ID, False otherwise.
        """
        try:
            ID.get_id(item, config)
            return True
        except LionIDError:
            return False


__all__ = [
    "INDICE_TYPE",
    "FIELD_NAME",
    "T",
    "LnID",
    "LionUndefinedType",
    "LN_UNDEFINED",
    "ID",
    "JsonValue",
    "BaseModel",
    "Field",
    "FieldInfo",
    "PydanticUndefined",
    "PrivateAttr",
    "ConfigDict",
    "SchemaModel",
    "FieldModel",
    "OperableModel",
    "Note",
    "BaseLionModel",
    "NewModelParams",
]
