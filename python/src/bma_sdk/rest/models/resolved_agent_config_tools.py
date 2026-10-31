from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.resolved_agent_config_tool import ResolvedAgentConfigTool


T = TypeVar("T", bound="ResolvedAgentConfigTools")


@_attrs_define
class ResolvedAgentConfigTools:
    """
    Attributes:
        tools (list['ResolvedAgentConfigTool']):
    """

    tools: list["ResolvedAgentConfigTool"]

    def to_dict(self) -> dict[str, Any]:
        tools = []
        for tools_item_data in self.tools:
            tools_item = tools_item_data.to_dict()
            tools.append(tools_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "tools": tools,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resolved_agent_config_tool import ResolvedAgentConfigTool

        d = dict(src_dict)
        tools = []
        _tools = d.pop("tools")
        for tools_item_data in _tools:
            tools_item = ResolvedAgentConfigTool.from_dict(tools_item_data)

            tools.append(tools_item)

        resolved_agent_config_tools = cls(
            tools=tools,
        )

        return resolved_agent_config_tools
