from typing import Literal, cast

ToolCallType = Literal["built_in", "custom", "mcp"]

TOOL_CALL_TYPE_VALUES: set[ToolCallType] = {
    "built_in",
    "custom",
    "mcp",
}


def check_tool_call_type(value: str) -> ToolCallType:
    if value in TOOL_CALL_TYPE_VALUES:
        return cast(ToolCallType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TOOL_CALL_TYPE_VALUES!r}"
    )
