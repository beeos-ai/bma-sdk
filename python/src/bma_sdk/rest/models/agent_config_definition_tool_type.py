from typing import Literal, cast

AgentConfigDefinitionToolType = Literal["built_in", "custom"]

AGENT_CONFIG_DEFINITION_TOOL_TYPE_VALUES: set[AgentConfigDefinitionToolType] = {
    "built_in",
    "custom",
}


def check_agent_config_definition_tool_type(
    value: str,
) -> AgentConfigDefinitionToolType:
    if value in AGENT_CONFIG_DEFINITION_TOOL_TYPE_VALUES:
        return cast(AgentConfigDefinitionToolType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_CONFIG_DEFINITION_TOOL_TYPE_VALUES!r}"
    )
