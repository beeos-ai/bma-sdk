from typing import Literal, cast

ToolResultEventEventKind = Literal["tool_result"]

TOOL_RESULT_EVENT_EVENT_KIND_VALUES: set[ToolResultEventEventKind] = {
    "tool_result",
}


def check_tool_result_event_event_kind(value: str) -> ToolResultEventEventKind:
    if value in TOOL_RESULT_EVENT_EVENT_KIND_VALUES:
        return cast(ToolResultEventEventKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TOOL_RESULT_EVENT_EVENT_KIND_VALUES!r}"
    )
