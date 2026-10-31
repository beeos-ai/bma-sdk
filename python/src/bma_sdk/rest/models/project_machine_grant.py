import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.project_machine_grant_source_kind import (
    ProjectMachineGrantSourceKind,
    check_project_machine_grant_source_kind,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="ProjectMachineGrant")


@_attrs_define
class ProjectMachineGrant:
    """
    Attributes:
        id (str):
        org_id (str):
        project_id (str): Project ID (proj_...).
        machine_id (str): Machine ID (mch_...).
        source_kind (ProjectMachineGrantSourceKind):
        description (str):
        metadata (Metadata): Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64 characters, values must be
            strings of up to 512 characters.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        project_machine_pool_grant_id (Union[None, Unset, str]):
    """

    id: str
    org_id: str
    project_id: str
    machine_id: str
    source_kind: ProjectMachineGrantSourceKind
    description: str
    metadata: "Metadata"
    created_at: datetime.datetime
    updated_at: datetime.datetime
    project_machine_pool_grant_id: Union[None, Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        machine_id = self.machine_id

        source_kind: str = self.source_kind

        description = self.description

        metadata = self.metadata.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        project_machine_pool_grant_id: Union[None, Unset, str]
        if isinstance(self.project_machine_pool_grant_id, Unset):
            project_machine_pool_grant_id = UNSET
        else:
            project_machine_pool_grant_id = self.project_machine_pool_grant_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "machine_id": machine_id,
                "source_kind": source_kind,
                "description": description,
                "metadata": metadata,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if project_machine_pool_grant_id is not UNSET:
            field_dict["project_machine_pool_grant_id"] = project_machine_pool_grant_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        machine_id = d.pop("machine_id")

        source_kind = check_project_machine_grant_source_kind(d.pop("source_kind"))

        description = d.pop("description")

        metadata = Metadata.from_dict(d.pop("metadata"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_project_machine_pool_grant_id(
            data: object,
        ) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_machine_pool_grant_id = _parse_project_machine_pool_grant_id(
            d.pop("project_machine_pool_grant_id", UNSET)
        )

        project_machine_grant = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            machine_id=machine_id,
            source_kind=source_kind,
            description=description,
            metadata=metadata,
            created_at=created_at,
            updated_at=updated_at,
            project_machine_pool_grant_id=project_machine_pool_grant_id,
        )

        return project_machine_grant
