from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.process_reconciliation_directive import ProcessReconciliationDirective


T = TypeVar("T", bound="DaemonRuntimeReconciliation")


@_attrs_define
class DaemonRuntimeReconciliation:
    """
    Attributes:
        processes (list['ProcessReconciliationDirective']):
    """

    processes: list["ProcessReconciliationDirective"]

    def to_dict(self) -> dict[str, Any]:
        processes = []
        for processes_item_data in self.processes:
            processes_item = processes_item_data.to_dict()
            processes.append(processes_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "processes": processes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.process_reconciliation_directive import (
            ProcessReconciliationDirective,
        )

        d = dict(src_dict)
        processes = []
        _processes = d.pop("processes")
        for processes_item_data in _processes:
            processes_item = ProcessReconciliationDirective.from_dict(
                processes_item_data
            )

            processes.append(processes_item)

        daemon_runtime_reconciliation = cls(
            processes=processes,
        )

        return daemon_runtime_reconciliation
