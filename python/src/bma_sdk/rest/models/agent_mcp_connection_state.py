from typing import Literal, cast

AgentMCPConnectionState = Literal["expired", "failed", "initializing", "ready"]

AGENT_MCP_CONNECTION_STATE_VALUES: set[AgentMCPConnectionState] = {
    "expired",
    "failed",
    "initializing",
    "ready",
}


def check_agent_mcp_connection_state(value: str) -> AgentMCPConnectionState:
    if value in AGENT_MCP_CONNECTION_STATE_VALUES:
        return cast(AgentMCPConnectionState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_MCP_CONNECTION_STATE_VALUES!r}"
    )
