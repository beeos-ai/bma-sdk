from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.file_scope_type import FileScopeType, check_file_scope_type

T = TypeVar("T", bound="FileScope")


@_attrs_define
class FileScope:
    """The session a session-scoped file belongs to.

    Attributes:
        type_ (FileScopeType):
        id (str):
    """

    type_: FileScopeType
    id: str

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        id = self.id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "id": id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_file_scope_type(d.pop("type"))

        id = d.pop("id")

        file_scope = cls(
            type_=type_,
            id=id,
        )

        return file_scope
