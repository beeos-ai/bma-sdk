from typing import Literal, cast

CreateAgentConfigRequestSourceFormat = Literal["json", "yaml"]

CREATE_AGENT_CONFIG_REQUEST_SOURCE_FORMAT_VALUES: set[
    CreateAgentConfigRequestSourceFormat
] = {
    "json",
    "yaml",
}


def check_create_agent_config_request_source_format(
    value: str,
) -> CreateAgentConfigRequestSourceFormat:
    if value in CREATE_AGENT_CONFIG_REQUEST_SOURCE_FORMAT_VALUES:
        return cast(CreateAgentConfigRequestSourceFormat, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CREATE_AGENT_CONFIG_REQUEST_SOURCE_FORMAT_VALUES!r}"
    )
