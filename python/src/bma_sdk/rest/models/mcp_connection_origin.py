from typing import Literal, cast

MCPConnectionOrigin = Literal["environment", "service"]

MCP_CONNECTION_ORIGIN_VALUES: set[MCPConnectionOrigin] = {
    "environment",
    "service",
}


def check_mcp_connection_origin(value: str) -> MCPConnectionOrigin:
    if value in MCP_CONNECTION_ORIGIN_VALUES:
        return cast(MCPConnectionOrigin, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MCP_CONNECTION_ORIGIN_VALUES!r}"
    )
