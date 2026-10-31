from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.tool_permission_selection import ToolPermissionSelection


T = TypeVar("T", bound="ResolvedAgentConfigTool")


@_attrs_define
class ResolvedAgentConfigTool:
    """
    Attributes:
        name (str):
        enabled (bool):
        permission (ToolPermissionSelection):
    """

    name: str
    enabled: bool
    permission: "ToolPermissionSelection"

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        enabled = self.enabled

        permission = self.permission.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "enabled": enabled,
                "permission": permission,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tool_permission_selection import ToolPermissionSelection

        d = dict(src_dict)
        name = d.pop("name")

        enabled = d.pop("enabled")

        permission = ToolPermissionSelection.from_dict(d.pop("permission"))

        resolved_agent_config_tool = cls(
            name=name,
            enabled=enabled,
            permission=permission,
        )

        return resolved_agent_config_tool
