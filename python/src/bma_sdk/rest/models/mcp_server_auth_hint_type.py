from typing import Literal, cast

MCPServerAuthHintType = Literal["bearer", "oauth"]

MCP_SERVER_AUTH_HINT_TYPE_VALUES: set[MCPServerAuthHintType] = {
    "bearer",
    "oauth",
}


def check_mcp_server_auth_hint_type(value: str) -> MCPServerAuthHintType:
    if value in MCP_SERVER_AUTH_HINT_TYPE_VALUES:
        return cast(MCPServerAuthHintType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MCP_SERVER_AUTH_HINT_TYPE_VALUES!r}"
    )
