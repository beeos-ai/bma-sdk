from typing import Literal, cast

ProcessReconciliationDirectiveDisposition = Literal[
    "close_preparation", "release", "retain", "start"
]

PROCESS_RECONCILIATION_DIRECTIVE_DISPOSITION_VALUES: set[
    ProcessReconciliationDirectiveDisposition
] = {
    "close_preparation",
    "release",
    "retain",
    "start",
}


def check_process_reconciliation_directive_disposition(
    value: str,
) -> ProcessReconciliationDirectiveDisposition:
    if value in PROCESS_RECONCILIATION_DIRECTIVE_DISPOSITION_VALUES:
        return cast(ProcessReconciliationDirectiveDisposition, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROCESS_RECONCILIATION_DIRECTIVE_DISPOSITION_VALUES!r}"
    )
