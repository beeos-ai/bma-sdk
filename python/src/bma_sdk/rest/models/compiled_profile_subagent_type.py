from typing import Literal, cast

CompiledProfileSubagentType = Literal["profile"]

COMPILED_PROFILE_SUBAGENT_TYPE_VALUES: set[CompiledProfileSubagentType] = {
    "profile",
}


def check_compiled_profile_subagent_type(value: str) -> CompiledProfileSubagentType:
    if value in COMPILED_PROFILE_SUBAGENT_TYPE_VALUES:
        return cast(CompiledProfileSubagentType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {COMPILED_PROFILE_SUBAGENT_TYPE_VALUES!r}"
    )
