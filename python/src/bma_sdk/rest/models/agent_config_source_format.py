from typing import Literal, cast

AgentConfigSourceFormat = Literal["json", "yaml"]

AGENT_CONFIG_SOURCE_FORMAT_VALUES: set[AgentConfigSourceFormat] = {
    "json",
    "yaml",
}


def check_agent_config_source_format(value: str) -> AgentConfigSourceFormat:
    if value in AGENT_CONFIG_SOURCE_FORMAT_VALUES:
        return cast(AgentConfigSourceFormat, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_CONFIG_SOURCE_FORMAT_VALUES!r}"
    )
