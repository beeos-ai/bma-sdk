from typing import Literal, cast

UpdateAgentConfigRequestSourceFormat = Literal["json", "yaml"]

UPDATE_AGENT_CONFIG_REQUEST_SOURCE_FORMAT_VALUES: set[
    UpdateAgentConfigRequestSourceFormat
] = {
    "json",
    "yaml",
}


def check_update_agent_config_request_source_format(
    value: str,
) -> UpdateAgentConfigRequestSourceFormat:
    if value in UPDATE_AGENT_CONFIG_REQUEST_SOURCE_FORMAT_VALUES:
        return cast(UpdateAgentConfigRequestSourceFormat, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {UPDATE_AGENT_CONFIG_REQUEST_SOURCE_FORMAT_VALUES!r}"
    )
