from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.machine import Machine
    from ..models.project_machine_grant import ProjectMachineGrant


T = TypeVar("T", bound="CreateProjectMachineGrantResponse")


@_attrs_define
class CreateProjectMachineGrantResponse:
    """
    Attributes:
        grant (ProjectMachineGrant):
        machine (Machine):
    """

    grant: "ProjectMachineGrant"
    machine: "Machine"

    def to_dict(self) -> dict[str, Any]:
        grant = self.grant.to_dict()

        machine = self.machine.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "grant": grant,
                "machine": machine,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.machine import Machine
        from ..models.project_machine_grant import ProjectMachineGrant

        d = dict(src_dict)
        grant = ProjectMachineGrant.from_dict(d.pop("grant"))

        machine = Machine.from_dict(d.pop("machine"))

        create_project_machine_grant_response = cls(
            grant=grant,
            machine=machine,
        )

        return create_project_machine_grant_response
