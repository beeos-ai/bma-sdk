from typing import Literal, cast

GetAgentConfigGeneratedSourceSourceFormat = Literal["json", "yaml"]

GET_AGENT_CONFIG_GENERATED_SOURCE_SOURCE_FORMAT_VALUES: set[
    GetAgentConfigGeneratedSourceSourceFormat
] = {
    "json",
    "yaml",
}


def check_get_agent_config_generated_source_source_format(
    value: str,
) -> GetAgentConfigGeneratedSourceSourceFormat:
    if value in GET_AGENT_CONFIG_GENERATED_SOURCE_SOURCE_FORMAT_VALUES:
        return cast(GetAgentConfigGeneratedSourceSourceFormat, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GET_AGENT_CONFIG_GENERATED_SOURCE_SOURCE_FORMAT_VALUES!r}"
    )
