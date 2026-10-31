from typing import Literal, cast

ProcessActionReconciliationClaimPosition = Literal["effect_committed", "terminal"]

PROCESS_ACTION_RECONCILIATION_CLAIM_POSITION_VALUES: set[
    ProcessActionReconciliationClaimPosition
] = {
    "effect_committed",
    "terminal",
}


def check_process_action_reconciliation_claim_position(
    value: str,
) -> ProcessActionReconciliationClaimPosition:
    if value in PROCESS_ACTION_RECONCILIATION_CLAIM_POSITION_VALUES:
        return cast(ProcessActionReconciliationClaimPosition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROCESS_ACTION_RECONCILIATION_CLAIM_POSITION_VALUES!r}"
    )
