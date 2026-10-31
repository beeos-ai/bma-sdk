from typing import Literal, cast

AgentConfigDefinitionModelCacheRetention = Literal["long", "none", "short"]

AGENT_CONFIG_DEFINITION_MODEL_CACHE_RETENTION_VALUES: set[
    AgentConfigDefinitionModelCacheRetention
] = {
    "long",
    "none",
    "short",
}


def check_agent_config_definition_model_cache_retention(
    value: str,
) -> AgentConfigDefinitionModelCacheRetention:
    if value in AGENT_CONFIG_DEFINITION_MODEL_CACHE_RETENTION_VALUES:
        return cast(AgentConfigDefinitionModelCacheRetention, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_CONFIG_DEFINITION_MODEL_CACHE_RETENTION_VALUES!r}"
    )
