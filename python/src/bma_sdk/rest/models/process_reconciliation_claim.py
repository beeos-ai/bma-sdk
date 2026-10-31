from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.process_reconciliation_claim_phase import (
    ProcessReconciliationClaimPhase,
    check_process_reconciliation_claim_phase,
)

if TYPE_CHECKING:
    from ..models.process_action_reconciliation_claim import (
        ProcessActionReconciliationClaim,
    )


T = TypeVar("T", bound="ProcessReconciliationClaim")


@_attrs_define
class ProcessReconciliationClaim:
    """
    Attributes:
        process_id (str):
        supervisor_instance_id (str):
        phase (ProcessReconciliationClaimPhase):
        supervisor_live (bool):
        execution_committed (bool):
        action_admission_closed (bool):
        resolved_action_seq (int):
        actions (list['ProcessActionReconciliationClaim']):
    """

    process_id: str
    supervisor_instance_id: str
    phase: ProcessReconciliationClaimPhase
    supervisor_live: bool
    execution_committed: bool
    action_admission_closed: bool
    resolved_action_seq: int
    actions: list["ProcessActionReconciliationClaim"]

    def to_dict(self) -> dict[str, Any]:
        process_id = self.process_id

        supervisor_instance_id = self.supervisor_instance_id

        phase: str = self.phase

        supervisor_live = self.supervisor_live

        execution_committed = self.execution_committed

        action_admission_closed = self.action_admission_closed

        resolved_action_seq = self.resolved_action_seq

        actions = []
        for actions_item_data in self.actions:
            actions_item = actions_item_data.to_dict()
            actions.append(actions_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "process_id": process_id,
                "supervisor_instance_id": supervisor_instance_id,
                "phase": phase,
                "supervisor_live": supervisor_live,
                "execution_committed": execution_committed,
                "action_admission_closed": action_admission_closed,
                "resolved_action_seq": resolved_action_seq,
                "actions": actions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.process_action_reconciliation_claim import (
            ProcessActionReconciliationClaim,
        )

        d = dict(src_dict)
        process_id = d.pop("process_id")

        supervisor_instance_id = d.pop("supervisor_instance_id")

        phase = check_process_reconciliation_claim_phase(d.pop("phase"))

        supervisor_live = d.pop("supervisor_live")

        execution_committed = d.pop("execution_committed")

        action_admission_closed = d.pop("action_admission_closed")

        resolved_action_seq = d.pop("resolved_action_seq")

        actions = []
        _actions = d.pop("actions")
        for actions_item_data in _actions:
            actions_item = ProcessActionReconciliationClaim.from_dict(actions_item_data)

            actions.append(actions_item)

        process_reconciliation_claim = cls(
            process_id=process_id,
            supervisor_instance_id=supervisor_instance_id,
            phase=phase,
            supervisor_live=supervisor_live,
            execution_committed=execution_committed,
            action_admission_closed=action_admission_closed,
            resolved_action_seq=resolved_action_seq,
            actions=actions,
        )

        return process_reconciliation_claim
