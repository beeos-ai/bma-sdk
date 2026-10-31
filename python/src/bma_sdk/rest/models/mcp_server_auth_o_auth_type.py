from typing import Literal, cast

MCPServerAuthOAuthType = Literal["oauth"]

MCP_SERVER_AUTH_O_AUTH_TYPE_VALUES: set[MCPServerAuthOAuthType] = {
    "oauth",
}


def check_mcp_server_auth_o_auth_type(value: str) -> MCPServerAuthOAuthType:
    if value in MCP_SERVER_AUTH_O_AUTH_TYPE_VALUES:
        return cast(MCPServerAuthOAuthType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MCP_SERVER_AUTH_O_AUTH_TYPE_VALUES!r}"
    )
