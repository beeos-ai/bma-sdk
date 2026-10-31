import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="CurrentUserOrg")


@_attrs_define
class CurrentUserOrg:
    """
    Attributes:
        id (str):
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        role (str): The authenticated user's role in this organization.
        created_at (datetime.datetime):
    """

    id: str
    name: str
    role: str
    created_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        role = self.role

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "name": name,
                "role": role,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        role = d.pop("role")

        created_at = isoparse(d.pop("created_at"))

        current_user_org = cls(
            id=id,
            name=name,
            role=role,
            created_at=created_at,
        )

        return current_user_org
