from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.memory_store_access import MemoryStoreAccess, check_memory_store_access

T = TypeVar("T", bound="CompiledMemoryStore")


@_attrs_define
class CompiledMemoryStore:
    """
    Attributes:
        id (str):
        access (MemoryStoreAccess):
    """

    id: str
    access: MemoryStoreAccess

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        access: str = self.access

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "access": access,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        access = check_memory_store_access(d.pop("access"))

        compiled_memory_store = cls(
            id=id,
            access=access,
        )

        return compiled_memory_store
