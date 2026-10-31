from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.process_action_reconciliation_directive_action_kind import (
    ProcessActionReconciliationDirectiveActionKind,
    check_process_action_reconciliation_directive_action_kind,
)
from ..models.process_action_reconciliation_directive_disposition import (
    ProcessActionReconciliationDirectiveDisposition,
    check_process_action_reconciliation_directive_disposition,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProcessActionReconciliationDirective")


@_attrs_define
class ProcessActionReconciliationDirective:
    """
    Attributes:
        process_action_id (str):
        seq (int):
        action_kind (ProcessActionReconciliationDirectiveActionKind):
        disposition (ProcessActionReconciliationDirectiveDisposition):
        payload (Union[Unset, Any]):
    """

    process_action_id: str
    seq: int
    action_kind: ProcessActionReconciliationDirectiveActionKind
    disposition: ProcessActionReconciliationDirectiveDisposition
    payload: Union[Unset, Any] = UNSET

    def to_dict(self) -> dict[str, Any]:
        process_action_id = self.process_action_id

        seq = self.seq

        action_kind: str = self.action_kind

        disposition: str = self.disposition

        payload = self.payload

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "process_action_id": process_action_id,
                "seq": seq,
                "action_kind": action_kind,
                "disposition": disposition,
            }
        )
        if payload is not UNSET:
            field_dict["payload"] = payload

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        process_action_id = d.pop("process_action_id")

        seq = d.pop("seq")

        action_kind = check_process_action_reconciliation_directive_action_kind(
            d.pop("action_kind")
        )

        disposition = check_process_action_reconciliation_directive_disposition(
            d.pop("disposition")
        )

        payload = d.pop("payload", UNSET)

        process_action_reconciliation_directive = cls(
            process_action_id=process_action_id,
            seq=seq,
            action_kind=action_kind,
            disposition=disposition,
            payload=payload,
        )

        return process_action_reconciliation_directive
