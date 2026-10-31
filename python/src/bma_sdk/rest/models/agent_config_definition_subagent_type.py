from typing import Literal, cast

AgentConfigDefinitionSubagentType = Literal["profile", "self"]

AGENT_CONFIG_DEFINITION_SUBAGENT_TYPE_VALUES: set[AgentConfigDefinitionSubagentType] = {
    "profile",
    "self",
}


def check_agent_config_definition_subagent_type(
    value: str,
) -> AgentConfigDefinitionSubagentType:
    if value in AGENT_CONFIG_DEFINITION_SUBAGENT_TYPE_VALUES:
        return cast(AgentConfigDefinitionSubagentType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_CONFIG_DEFINITION_SUBAGENT_TYPE_VALUES!r}"
    )
