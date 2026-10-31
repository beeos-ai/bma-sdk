from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.machine_summary_fields import MachineSummaryFields
    from ..models.project_machine_grant import ProjectMachineGrant


T = TypeVar("T", bound="ProjectMachineGrantListItem")


@_attrs_define
class ProjectMachineGrantListItem:
    """
    Attributes:
        grant (ProjectMachineGrant):
        machine (MachineSummaryFields): Shared machine fields composed into machine response schemas. Composing schemas
            close their final shape with unevaluatedProperties.
    """

    grant: "ProjectMachineGrant"
    machine: "MachineSummaryFields"

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
        from ..models.machine_summary_fields import MachineSummaryFields
        from ..models.project_machine_grant import ProjectMachineGrant

        d = dict(src_dict)
        grant = ProjectMachineGrant.from_dict(d.pop("grant"))

        machine = MachineSummaryFields.from_dict(d.pop("machine"))

        project_machine_grant_list_item = cls(
            grant=grant,
            machine=machine,
        )

        return project_machine_grant_list_item
