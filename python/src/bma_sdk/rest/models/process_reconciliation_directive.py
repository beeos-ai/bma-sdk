from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.process_reconciliation_directive_disposition import (
    ProcessReconciliationDirectiveDisposition,
    check_process_reconciliation_directive_disposition,
)

if TYPE_CHECKING:
    from ..models.process_action_reconciliation_directive import (
        ProcessActionReconciliationDirective,
    )


T = TypeVar("T", bound="ProcessReconciliationDirective")


@_attrs_define
class ProcessReconciliationDirective:
    """
    Attributes:
        process_id (str):
        supervisor_instance_id (str):
        disposition (ProcessReconciliationDirectiveDisposition):
        actions (list['ProcessActionReconciliationDirective']):
    """

    process_id: str
    supervisor_instance_id: str
    disposition: ProcessReconciliationDirectiveDisposition
    actions: list["ProcessActionReconciliationDirective"]

    def to_dict(self) -> dict[str, Any]:
        process_id = self.process_id

        supervisor_instance_id = self.supervisor_instance_id

        disposition: str = self.disposition

        actions = []
        for actions_item_data in self.actions:
            actions_item = actions_item_data.to_dict()
            actions.append(actions_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "process_id": process_id,
                "supervisor_instance_id": supervisor_instance_id,
                "disposition": disposition,
                "actions": actions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.process_action_reconciliation_directive import (
            ProcessActionReconciliationDirective,
        )

        d = dict(src_dict)
        process_id = d.pop("process_id")

        supervisor_instance_id = d.pop("supervisor_instance_id")

        disposition = check_process_reconciliation_directive_disposition(
            d.pop("disposition")
        )

        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:
            actions_item = ProcessActionReconciliationDirective.from_dict(
                actions_item_data
            )

            actions.append(actions_item)

        process_reconciliation_directive = cls(
            process_id=process_id,
            supervisor_instance_id=supervisor_instance_id,
            disposition=disposition,
            actions=actions,
        )

        return process_reconciliation_directive
