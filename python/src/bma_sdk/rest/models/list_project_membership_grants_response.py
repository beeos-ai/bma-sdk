from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.project_membership_grant import ProjectMembershipGrant


T = TypeVar("T", bound="ListProjectMembershipGrantsResponse")


@_attrs_define
class ListProjectMembershipGrantsResponse:
    """
    Attributes:
        data (list['ProjectMembershipGrant']):
    """

    data: list["ProjectMembershipGrant"]

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_membership_grant import ProjectMembershipGrant

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = ProjectMembershipGrant.from_dict(data_item_data)

            data.append(data_item)

        list_project_membership_grants_response = cls(
            data=data,
        )

        return list_project_membership_grants_response
