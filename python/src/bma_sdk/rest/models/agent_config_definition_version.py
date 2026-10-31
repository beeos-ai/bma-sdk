from typing import Literal, cast

AgentConfigDefinitionVersion = Literal["v1"]

AGENT_CONFIG_DEFINITION_VERSION_VALUES: set[AgentConfigDefinitionVersion] = {
    "v1",
}


def check_agent_config_definition_version(value: str) -> AgentConfigDefinitionVersion:
    if value in AGENT_CONFIG_DEFINITION_VERSION_VALUES:
        return cast(AgentConfigDefinitionVersion, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_CONFIG_DEFINITION_VERSION_VALUES!r}"
    )
