from typing import Literal, cast

ProcessReconciliationClaimPhase = Literal[
    "accepted", "prepared", "preparing", "terminal"
]

PROCESS_RECONCILIATION_CLAIM_PHASE_VALUES: set[ProcessReconciliationClaimPhase] = {
    "accepted",
    "prepared",
    "preparing",
    "terminal",
}


def check_process_reconciliation_claim_phase(
    value: str,
) -> ProcessReconciliationClaimPhase:
    if value in PROCESS_RECONCILIATION_CLAIM_PHASE_VALUES:
        return cast(ProcessReconciliationClaimPhase, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROCESS_RECONCILIATION_CLAIM_PHASE_VALUES!r}"
    )
