from typing import Literal, cast

CompiledToolType = Literal["built_in", "custom"]

COMPILED_TOOL_TYPE_VALUES: set[CompiledToolType] = {
    "built_in",
    "custom",
}


def check_compiled_tool_type(value: str) -> CompiledToolType:
    if value in COMPILED_TOOL_TYPE_VALUES:
        return cast(CompiledToolType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {COMPILED_TOOL_TYPE_VALUES!r}"
    )
