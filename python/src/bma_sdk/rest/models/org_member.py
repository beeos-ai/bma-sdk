import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="OrgMember")


@_attrs_define
class OrgMember:
    """
    Attributes:
        user_id (str):
        email (str): The member's primary verified email, or an empty string if none.
        display_name (str):
        role (str): The member's role in the organization (owner, admin, or member).
        created_at (datetime.datetime):
    """

    user_id: str
    email: str
    display_name: str
    role: str
    created_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        user_id = self.user_id

        email = self.email

        display_name = self.display_name

        role = self.role

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "user_id": user_id,
                "email": email,
                "display_name": display_name,
                "role": role,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_id = d.pop("user_id")

        email = d.pop("email")

        display_name = d.pop("display_name")

        role = d.pop("role")

        created_at = isoparse(d.pop("created_at"))

        org_member = cls(
            user_id=user_id,
            email=email,
            display_name=display_name,
            role=role,
            created_at=created_at,
        )

        return org_member
