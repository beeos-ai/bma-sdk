from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UpdateOrgMemberRequest")


@_attrs_define
class UpdateOrgMemberRequest:
    """
    Attributes:
        role (str): The member's new org role (admin or member).
    """

    role: str

    def to_dict(self) -> dict[str, Any]:
        role = self.role

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = d.pop("role")

        update_org_member_request = cls(
            role=role,
        )

        return update_org_member_request
