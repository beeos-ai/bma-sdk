from typing import Literal, cast

CompiledSelfSubagentType = Literal["self"]

COMPILED_SELF_SUBAGENT_TYPE_VALUES: set[CompiledSelfSubagentType] = {
    "self",
}


def check_compiled_self_subagent_type(value: str) -> CompiledSelfSubagentType:
    if value in COMPILED_SELF_SUBAGENT_TYPE_VALUES:
        return cast(CompiledSelfSubagentType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {COMPILED_SELF_SUBAGENT_TYPE_VALUES!r}"
    )
