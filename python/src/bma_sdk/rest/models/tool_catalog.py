from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.tool_catalog_entry import ToolCatalogEntry
    from ..models.tool_permission_profile import ToolPermissionProfile


T = TypeVar("T", bound="ToolCatalog")


@_attrs_define
class ToolCatalog:
    """
    Attributes:
        built_in_tools (list['ToolCatalogEntry']):
        custom_tool_permissions (ToolPermissionProfile):
        mcp_tool_permissions (ToolPermissionProfile):
    """

    built_in_tools: list["ToolCatalogEntry"]
    custom_tool_permissions: "ToolPermissionProfile"
    mcp_tool_permissions: "ToolPermissionProfile"

    def to_dict(self) -> dict[str, Any]:
        built_in_tools = []
        for built_in_tools_item_data in self.built_in_tools:
            built_in_tools_item = built_in_tools_item_data.to_dict()
            built_in_tools.append(built_in_tools_item)

        custom_tool_permissions = self.custom_tool_permissions.to_dict()

        mcp_tool_permissions = self.mcp_tool_permissions.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "built_in_tools": built_in_tools,
                "custom_tool_permissions": custom_tool_permissions,
                "mcp_tool_permissions": mcp_tool_permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tool_catalog_entry import ToolCatalogEntry
        from ..models.tool_permission_profile import ToolPermissionProfile

        d = dict(src_dict)
        built_in_tools = []
        _built_in_tools = d.pop("built_in_tools")
        for built_in_tools_item_data in _built_in_tools:
            built_in_tools_item = ToolCatalogEntry.from_dict(built_in_tools_item_data)

            built_in_tools.append(built_in_tools_item)

        custom_tool_permissions = ToolPermissionProfile.from_dict(
            d.pop("custom_tool_permissions")
        )

        mcp_tool_permissions = ToolPermissionProfile.from_dict(
            d.pop("mcp_tool_permissions")
        )

        tool_catalog = cls(
            built_in_tools=built_in_tools,
            custom_tool_permissions=custom_tool_permissions,
            mcp_tool_permissions=mcp_tool_permissions,
        )

        return tool_catalog
