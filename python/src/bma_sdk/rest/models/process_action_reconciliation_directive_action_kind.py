from typing import Literal, cast

ProcessActionReconciliationDirectiveActionKind = Literal[
    "interrupt", "read", "terminate", "write"
]

PROCESS_ACTION_RECONCILIATION_DIRECTIVE_ACTION_KIND_VALUES: set[
    ProcessActionReconciliationDirectiveActionKind
] = {
    "interrupt",
    "read",
    "terminate",
    "write",
}


def check_process_action_reconciliation_directive_action_kind(
    value: str,
) -> ProcessActionReconciliationDirectiveActionKind:
    if value in PROCESS_ACTION_RECONCILIATION_DIRECTIVE_ACTION_KIND_VALUES:
        return cast(ProcessActionReconciliationDirectiveActionKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROCESS_ACTION_RECONCILIATION_DIRECTIVE_ACTION_KIND_VALUES!r}"
    )
