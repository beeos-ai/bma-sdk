import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.memory_regular_file_type import (
    MemoryRegularFileType,
    check_memory_regular_file_type,
)

T = TypeVar("T", bound="MemoryRegularFile")


@_attrs_define
class MemoryRegularFile:
    """
    Attributes:
        path (str):
        type_ (MemoryRegularFileType):
        size_bytes (int):
        modified_at (datetime.datetime):
    """

    path: str
    type_: MemoryRegularFileType
    size_bytes: int
    modified_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        type_: str = self.type_

        size_bytes = self.size_bytes

        modified_at = self.modified_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "path": path,
                "type": type_,
                "size_bytes": size_bytes,
                "modified_at": modified_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        type_ = check_memory_regular_file_type(d.pop("type"))

        size_bytes = d.pop("size_bytes")

        modified_at = isoparse(d.pop("modified_at"))

        memory_regular_file = cls(
            path=path,
            type_=type_,
            size_bytes=size_bytes,
            modified_at=modified_at,
        )

        return memory_regular_file
