from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.machine_pool_summary import MachinePoolSummary
    from ..models.project_machine_pool_grant import ProjectMachinePoolGrant


T = TypeVar("T", bound="ProjectMachinePoolGrantListItem")


@_attrs_define
class ProjectMachinePoolGrantListItem:
    """
    Attributes:
        grant (ProjectMachinePoolGrant):
        machine_pool (MachinePoolSummary):
    """

    grant: "ProjectMachinePoolGrant"
    machine_pool: "MachinePoolSummary"

    def to_dict(self) -> dict[str, Any]:
        grant = self.grant.to_dict()

        machine_pool = self.machine_pool.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "grant": grant,
                "machine_pool": machine_pool,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.machine_pool_summary import MachinePoolSummary
        from ..models.project_machine_pool_grant import ProjectMachinePoolGrant

        d = dict(src_dict)
        grant = ProjectMachinePoolGrant.from_dict(d.pop("grant"))

        machine_pool = MachinePoolSummary.from_dict(d.pop("machine_pool"))

        project_machine_pool_grant_list_item = cls(
            grant=grant,
            machine_pool=machine_pool,
        )

        return project_machine_pool_grant_list_item
