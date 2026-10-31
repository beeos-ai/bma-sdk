import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="ProjectMembershipGrant")


@_attrs_define
class ProjectMembershipGrant:
    """
    Attributes:
        project_id (str): Project ID (proj_...).
        project_name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        role (str): The member's role on the project (admin, developer, operator, or viewer).
        created_at (datetime.datetime):
    """

    project_id: str
    project_name: str
    role: str
    created_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        project_name = self.project_name

        role = self.role

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "project_id": project_id,
                "project_name": project_name,
                "role": role,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        project_name = d.pop("project_name")

        role = d.pop("role")

        created_at = isoparse(d.pop("created_at"))

        project_membership_grant = cls(
            project_id=project_id,
            project_name=project_name,
            role=role,
            created_at=created_at,
        )

        return project_membership_grant
