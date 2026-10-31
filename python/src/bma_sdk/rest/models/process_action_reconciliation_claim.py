from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.process_action_reconciliation_claim_action_kind import (
    ProcessActionReconciliationClaimActionKind,
    check_process_action_reconciliation_claim_action_kind,
)
from ..models.process_action_reconciliation_claim_position import (
    ProcessActionReconciliationClaimPosition,
    check_process_action_reconciliation_claim_position,
)

T = TypeVar("T", bound="ProcessActionReconciliationClaim")


@_attrs_define
class ProcessActionReconciliationClaim:
    """
    Attributes:
        process_action_id (str):
        seq (int):
        action_kind (ProcessActionReconciliationClaimActionKind):
        position (ProcessActionReconciliationClaimPosition):
    """

    process_action_id: str
    seq: int
    action_kind: ProcessActionReconciliationClaimActionKind
    position: ProcessActionReconciliationClaimPosition

    def to_dict(self) -> dict[str, Any]:
        process_action_id = self.process_action_id

        seq = self.seq

        action_kind: str = self.action_kind

        position: str = self.position

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "process_action_id": process_action_id,
                "seq": seq,
                "action_kind": action_kind,
                "position": position,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        process_action_id = d.pop("process_action_id")

        seq = d.pop("seq")

        action_kind = check_process_action_reconciliation_claim_action_kind(
            d.pop("action_kind")
        )

        position = check_process_action_reconciliation_claim_position(d.pop("position"))

        process_action_reconciliation_claim = cls(
            process_action_id=process_action_id,
            seq=seq,
            action_kind=action_kind,
            position=position,
        )

        return process_action_reconciliation_claim
