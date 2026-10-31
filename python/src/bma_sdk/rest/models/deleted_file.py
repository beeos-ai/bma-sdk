from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.deleted_file_type import DeletedFileType, check_deleted_file_type

T = TypeVar("T", bound="DeletedFile")


@_attrs_define
class DeletedFile:
    """
    Attributes:
        id (str): File ID (file_...).
        type_ (DeletedFileType):
    """

    id: str
    type_: DeletedFileType

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_: str = self.type_

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        type_ = check_deleted_file_type(d.pop("type"))

        deleted_file = cls(
            id=id,
            type_=type_,
        )

        return deleted_file
