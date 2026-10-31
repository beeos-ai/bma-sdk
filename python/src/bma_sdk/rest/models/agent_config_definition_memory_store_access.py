from typing import Literal, cast

AgentConfigDefinitionMemoryStoreAccess = Literal["read", "read_write"]

AGENT_CONFIG_DEFINITION_MEMORY_STORE_ACCESS_VALUES: set[
    AgentConfigDefinitionMemoryStoreAccess
] = {
    "read",
    "read_write",
}


def check_agent_config_definition_memory_store_access(
    value: str,
) -> AgentConfigDefinitionMemoryStoreAccess:
    if value in AGENT_CONFIG_DEFINITION_MEMORY_STORE_ACCESS_VALUES:
        return cast(AgentConfigDefinitionMemoryStoreAccess, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_CONFIG_DEFINITION_MEMORY_STORE_ACCESS_VALUES!r}"
    )
