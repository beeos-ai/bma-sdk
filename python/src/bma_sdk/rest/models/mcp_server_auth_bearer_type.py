from typing import Literal, cast

MCPServerAuthBearerType = Literal["bearer"]

MCP_SERVER_AUTH_BEARER_TYPE_VALUES: set[MCPServerAuthBearerType] = {
    "bearer",
}


def check_mcp_server_auth_bearer_type(value: str) -> MCPServerAuthBearerType:
    if value in MCP_SERVER_AUTH_BEARER_TYPE_VALUES:
        return cast(MCPServerAuthBearerType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MCP_SERVER_AUTH_BEARER_TYPE_VALUES!r}"
    )
