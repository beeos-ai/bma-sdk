from typing import Literal, cast

ProcessActionReconciliationDirectiveDisposition = Literal[
    "apply", "release", "retain", "settle"
]

PROCESS_ACTION_RECONCILIATION_DIRECTIVE_DISPOSITION_VALUES: set[
    ProcessActionReconciliationDirectiveDisposition
] = {
    "apply",
    "release",
    "retain",
    "settle",
}


def check_process_action_reconciliation_directive_disposition(
    value: str,
) -> ProcessActionReconciliationDirectiveDisposition:
    if value in PROCESS_ACTION_RECONCILIATION_DIRECTIVE_DISPOSITION_VALUES:
        return cast(ProcessActionReconciliationDirectiveDisposition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROCESS_ACTION_RECONCILIATION_DIRECTIVE_DISPOSITION_VALUES!r}"
    )
