from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.mcp_server_info import MCPServerInfo
    from ..models.mcp_server_tool import MCPServerTool


T = TypeVar("T", bound="MCPServerToolsResponse")


@_attrs_define
class MCPServerToolsResponse:
    """
    Attributes:
        protocol_version (str): MCP protocol version negotiated with the server.
        server_info (MCPServerInfo):
        tools (list['MCPServerTool']):
    """

    protocol_version: str
    server_info: "MCPServerInfo"
    tools: list["MCPServerTool"]

    def to_dict(self) -> dict[str, Any]:
        protocol_version = self.protocol_version

        server_info = self.server_info.to_dict()

        tools = []
        for tools_item_data in self.tools:
            tools_item = tools_item_data.to_dict()
            tools.append(tools_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "protocol_version": protocol_version,
                "server_info": server_info,
                "tools": tools,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mcp_server_info import MCPServerInfo
        from ..models.mcp_server_tool import MCPServerTool

        d = dict(src_dict)
        protocol_version = d.pop("protocol_version")

        server_info = MCPServerInfo.from_dict(d.pop("server_info"))

        tools = []
        _tools = d.pop("tools")
        for tools_item_data in _tools:
            tools_item = MCPServerTool.from_dict(tools_item_data)

            tools.append(tools_item)

        mcp_server_tools_response = cls(
            protocol_version=protocol_version,
            server_info=server_info,
            tools=tools,
        )

        return mcp_server_tools_response
