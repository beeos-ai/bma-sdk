from typing import Literal, cast

AgentConfigDefinitionSubagentModelCacheRetention = Literal["long", "none", "short"]

AGENT_CONFIG_DEFINITION_SUBAGENT_MODEL_CACHE_RETENTION_VALUES: set[
    AgentConfigDefinitionSubagentModelCacheRetention
] = {
    "long",
    "none",
    "short",
}


def check_agent_config_definition_subagent_model_cache_retention(
    value: str,
) -> AgentConfigDefinitionSubagentModelCacheRetention:
    if value in AGENT_CONFIG_DEFINITION_SUBAGENT_MODEL_CACHE_RETENTION_VALUES:
        return cast(AgentConfigDefinitionSubagentModelCacheRetention, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_CONFIG_DEFINITION_SUBAGENT_MODEL_CACHE_RETENTION_VALUES!r}"
    )
