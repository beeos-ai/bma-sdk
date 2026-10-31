from typing import Literal, cast

MCPServerAuthSigV4Type = Literal["sigv4"]

MCP_SERVER_AUTH_SIG_V4_TYPE_VALUES: set[MCPServerAuthSigV4Type] = {
    "sigv4",
}


def check_mcp_server_auth_sig_v4_type(value: str) -> MCPServerAuthSigV4Type:
    if value in MCP_SERVER_AUTH_SIG_V4_TYPE_VALUES:
        return cast(MCPServerAuthSigV4Type, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MCP_SERVER_AUTH_SIG_V4_TYPE_VALUES!r}"
    )
