from typing import Literal, cast

ToolCallState = Literal[
    "awaiting_authorization",
    "awaiting_permission",
    "completed",
    "ready",
    "running",
    "waiting",
]

TOOL_CALL_STATE_VALUES: set[ToolCallState] = {
    "awaiting_authorization",
    "awaiting_permission",
    "completed",
    "ready",
    "running",
    "waiting",
}


def check_tool_call_state(value: str) -> ToolCallState:
    if value in TOOL_CALL_STATE_VALUES:
        return cast(ToolCallState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TOOL_CALL_STATE_VALUES!r}"
    )
