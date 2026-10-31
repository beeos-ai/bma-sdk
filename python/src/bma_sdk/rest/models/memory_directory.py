import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.memory_directory_type import (
    MemoryDirectoryType,
    check_memory_directory_type,
)

T = TypeVar("T", bound="MemoryDirectory")


@_attrs_define
class MemoryDirectory:
    """
    Attributes:
        path (str):
        type_ (MemoryDirectoryType):
        modified_at (datetime.datetime):
    """

    path: str
    type_: MemoryDirectoryType
    modified_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        type_: str = self.type_

        modified_at = self.modified_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "path": path,
                "type": type_,
                "modified_at": modified_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        type_ = check_memory_directory_type(d.pop("type"))

        modified_at = isoparse(d.pop("modified_at"))

        memory_directory = cls(
            path=path,
            type_=type_,
            modified_at=modified_at,
        )

        return memory_directory
