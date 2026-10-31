import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.management_kind import ManagementKind, check_management_kind

T = TypeVar("T", bound="MachinePoolSummary")


@_attrs_define
class MachinePoolSummary:
    """
    Attributes:
        id (str): Machine pool ID (mpo_...).
        org_id (str):
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        management_kind (ManagementKind): Lifecycle owner. Tenant-managed resources can be changed through tenant APIs.
            Cluster-managed resources are installed and lifecycle-managed by the control plane; individual APIs may
            explicitly expose tenant-editable settings.
        description (str):
        provider (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: str
    org_id: str
    name: str
    management_kind: ManagementKind
    description: str
    provider: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        name = self.name

        management_kind: str = self.management_kind

        description = self.description

        provider = self.provider

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "name": name,
                "management_kind": management_kind,
                "description": description,
                "provider": provider,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        name = d.pop("name")

        management_kind = check_management_kind(d.pop("management_kind"))

        description = d.pop("description")

        provider = d.pop("provider")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        machine_pool_summary = cls(
            id=id,
            org_id=org_id,
            name=name,
            management_kind=management_kind,
            description=description,
            provider=provider,
            created_at=created_at,
            updated_at=updated_at,
        )

        return machine_pool_summary
