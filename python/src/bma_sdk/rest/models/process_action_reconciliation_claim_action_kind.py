from typing import Literal, cast

ProcessActionReconciliationClaimActionKind = Literal["interrupt", "terminate", "write"]

PROCESS_ACTION_RECONCILIATION_CLAIM_ACTION_KIND_VALUES: set[
    ProcessActionReconciliationClaimActionKind
] = {
    "interrupt",
    "terminate",
    "write",
}


def check_process_action_reconciliation_claim_action_kind(
    value: str,
) -> ProcessActionReconciliationClaimActionKind:
    if value in PROCESS_ACTION_RECONCILIATION_CLAIM_ACTION_KIND_VALUES:
        return cast(ProcessActionReconciliationClaimActionKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROCESS_ACTION_RECONCILIATION_CLAIM_ACTION_KIND_VALUES!r}"
    )
