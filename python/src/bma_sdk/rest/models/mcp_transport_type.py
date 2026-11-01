from typing import Literal, cast

MCPTransportType = Literal["http", "stdio"]

MCP_TRANSPORT_TYPE_VALUES: set[MCPTransportType] = {
    "http",
    "stdio",
}


def check_mcp_transport_type(value: str) -> MCPTransportType:
    if value in MCP_TRANSPORT_TYPE_VALUES:
        return cast(MCPTransportType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MCP_TRANSPORT_TYPE_VALUES!r}"
    )
