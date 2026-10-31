from typing import Literal, cast

MCPServerBMAAuthType = Literal["bearer", "oauth", "sigv4"]

MCP_SERVER_BMA_AUTH_TYPE_VALUES: set[MCPServerBMAAuthType] = {
    "bearer",
    "oauth",
    "sigv4",
}


def check_mcp_server_bma_auth_type(value: str) -> MCPServerBMAAuthType:
    if value in MCP_SERVER_BMA_AUTH_TYPE_VALUES:
        return cast(MCPServerBMAAuthType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MCP_SERVER_BMA_AUTH_TYPE_VALUES!r}"
    )
