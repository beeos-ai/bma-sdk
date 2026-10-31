import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="OrganizationMembership")


@_attrs_define
class OrganizationMembership:
    """
    Attributes:
        org_id (str):
        user_id (str):
        role (str):
        created_at (datetime.datetime):
    """

    org_id: str
    user_id: str
    role: str
    created_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        org_id = self.org_id

        user_id = self.user_id

        role = self.role

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "org_id": org_id,
                "user_id": user_id,
                "role": role,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        org_id = d.pop("org_id")

        user_id = d.pop("user_id")

        role = d.pop("role")

        created_at = isoparse(d.pop("created_at"))

        organization_membership = cls(
            org_id=org_id,
            user_id=user_id,
            role=role,
            created_at=created_at,
        )

        return organization_membership
