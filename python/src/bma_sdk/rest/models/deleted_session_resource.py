from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.deleted_session_resource_type import (
    DeletedSessionResourceType,
    check_deleted_session_resource_type,
)

T = TypeVar("T", bound="DeletedSessionResource")


@_attrs_define
class DeletedSessionResource:
    """
    Attributes:
        id (str):
        type_ (DeletedSessionResourceType):
    """

    id: str
    type_: DeletedSessionResourceType

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

        type_ = check_deleted_session_resource_type(d.pop("type"))

        deleted_session_resource = cls(
            id=id,
            type_=type_,
        )

        return deleted_session_resource
