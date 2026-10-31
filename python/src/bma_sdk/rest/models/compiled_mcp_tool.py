from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tool_permission_selection import ToolPermissionSelection


T = TypeVar("T", bound="CompiledMCPTool")


@_attrs_define
class CompiledMCPTool:
    """
    Attributes:
        enabled (Union[Unset, bool]):
        permission (Union[Unset, ToolPermissionSelection]):
        deferred (Union[Unset, bool]):
    """

    enabled: Union[Unset, bool] = UNSET
    permission: Union[Unset, "ToolPermissionSelection"] = UNSET
    deferred: Union[Unset, bool] = UNSET

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        permission: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.permission, Unset):
            permission = self.permission.to_dict()

        deferred = self.deferred

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if permission is not UNSET:
            field_dict["permission"] = permission
        if deferred is not UNSET:
            field_dict["deferred"] = deferred

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tool_permission_selection import ToolPermissionSelection

        d = dict(src_dict)
        enabled = d.pop("enabled", UNSET)

        _permission = d.pop("permission", UNSET)
        permission: Union[Unset, ToolPermissionSelection]
        if isinstance(_permission, Unset):
            permission = UNSET
        else:
            permission = ToolPermissionSelection.from_dict(_permission)

        deferred = d.pop("deferred", UNSET)

        compiled_mcp_tool = cls(
            enabled=enabled,
            permission=permission,
            deferred=deferred,
        )

        return compiled_mcp_tool
