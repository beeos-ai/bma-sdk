import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="OrgOverviewProjectActivity")


@_attrs_define
class OrgOverviewProjectActivity:
    """
    Attributes:
        project_id (str): Project ID (proj_...).
        last_active_at (datetime.datetime):
    """

    project_id: str
    last_active_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        last_active_at = self.last_active_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "project_id": project_id,
                "last_active_at": last_active_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        last_active_at = isoparse(d.pop("last_active_at"))

        org_overview_project_activity = cls(
            project_id=project_id,
            last_active_at=last_active_at,
        )

        return org_overview_project_activity
