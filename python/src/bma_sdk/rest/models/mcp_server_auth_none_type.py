from typing import Literal, cast

MCPServerAuthNoneType = Literal["none"]

MCP_SERVER_AUTH_NONE_TYPE_VALUES: set[MCPServerAuthNoneType] = {
    "none",
}


def check_mcp_server_auth_none_type(value: str) -> MCPServerAuthNoneType:
    if value in MCP_SERVER_AUTH_NONE_TYPE_VALUES:
        return cast(MCPServerAuthNoneType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MCP_SERVER_AUTH_NONE_TYPE_VALUES!r}"
    )
