from typing import Literal, cast

ToolCallOutcome = Literal["canceled", "denied", "failed", "succeeded"]

TOOL_CALL_OUTCOME_VALUES: set[ToolCallOutcome] = {
    "canceled",
    "denied",
    "failed",
    "succeeded",
}


def check_tool_call_outcome(value: str) -> ToolCallOutcome:
    if value in TOOL_CALL_OUTCOME_VALUES:
        return cast(ToolCallOutcome, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TOOL_CALL_OUTCOME_VALUES!r}"
    )
