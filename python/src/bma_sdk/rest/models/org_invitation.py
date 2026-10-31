import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="OrgInvitation")


@_attrs_define
class OrgInvitation:
    """
    Attributes:
        id (str):
        org_id (str):
        org_name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        email (str):
        org_role (str):
        created_at (datetime.datetime):
    """

    id: str
    org_id: str
    org_name: str
    email: str
    org_role: str
    created_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        org_name = self.org_name

        email = self.email

        org_role = self.org_role

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "org_name": org_name,
                "email": email,
                "org_role": org_role,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        org_name = d.pop("org_name")

        email = d.pop("email")

        org_role = d.pop("org_role")

        created_at = isoparse(d.pop("created_at"))

        org_invitation = cls(
            id=id,
            org_id=org_id,
            org_name=org_name,
            email=email,
            org_role=org_role,
            created_at=created_at,
        )

        return org_invitation
