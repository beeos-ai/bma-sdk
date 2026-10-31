from typing import Literal, cast

AgentConfigDefinitionMCPAuthType = Literal["bearer", "oauth", "sigv4"]

AGENT_CONFIG_DEFINITION_MCP_AUTH_TYPE_VALUES: set[AgentConfigDefinitionMCPAuthType] = {
    "bearer",
    "oauth",
    "sigv4",
}


def check_agent_config_definition_mcp_auth_type(
    value: str,
) -> AgentConfigDefinitionMCPAuthType:
    if value in AGENT_CONFIG_DEFINITION_MCP_AUTH_TYPE_VALUES:
        return cast(AgentConfigDefinitionMCPAuthType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_CONFIG_DEFINITION_MCP_AUTH_TYPE_VALUES!r}"
    )
