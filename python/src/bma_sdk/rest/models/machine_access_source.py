from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.machine_access_source_kind import (
    MachineAccessSourceKind,
    check_machine_access_source_kind,
)
from ..models.project_machine_grant_source_kind import (
    ProjectMachineGrantSourceKind,
    check_project_machine_grant_source_kind,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="MachineAccessSource")


@_attrs_define
class MachineAccessSource:
    """
    Attributes:
        kind (MachineAccessSourceKind):
        project_id (Union[Unset, str]): Project ID (proj_...).
        grant_id (Union[Unset, str]):
        grant_source_kind (Union[Unset, ProjectMachineGrantSourceKind]):
    """

    kind: MachineAccessSourceKind
    project_id: Union[Unset, str] = UNSET
    grant_id: Union[Unset, str] = UNSET
    grant_source_kind: Union[Unset, ProjectMachineGrantSourceKind] = UNSET

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        project_id = self.project_id

        grant_id = self.grant_id

        grant_source_kind: Union[Unset, str] = UNSET
        if not isinstance(self.grant_source_kind, Unset):
            grant_source_kind = self.grant_source_kind

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
            }
        )
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if grant_id is not UNSET:
            field_dict["grant_id"] = grant_id
        if grant_source_kind is not UNSET:
            field_dict["grant_source_kind"] = grant_source_kind

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_machine_access_source_kind(d.pop("kind"))

        project_id = d.pop("project_id", UNSET)

        grant_id = d.pop("grant_id", UNSET)

        _grant_source_kind = d.pop("grant_source_kind", UNSET)
        grant_source_kind: Union[Unset, ProjectMachineGrantSourceKind]
        if isinstance(_grant_source_kind, Unset):
            grant_source_kind = UNSET
        else:
            grant_source_kind = check_project_machine_grant_source_kind(
                _grant_source_kind
            )

        machine_access_source = cls(
            kind=kind,
            project_id=project_id,
            grant_id=grant_id,
            grant_source_kind=grant_source_kind,
        )

        return machine_access_source
