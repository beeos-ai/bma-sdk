from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.tool_permission_mode import ToolPermissionMode
    from ..models.tool_permission_selection import ToolPermissionSelection


T = TypeVar("T", bound="ToolPermissionProfile")


@_attrs_define
class ToolPermissionProfile:
    """
    Attributes:
        default_permission (ToolPermissionSelection):
        permission_modes (list['ToolPermissionMode']):
    """

    default_permission: "ToolPermissionSelection"
    permission_modes: list["ToolPermissionMode"]

    def to_dict(self) -> dict[str, Any]:
        default_permission = self.default_permission.to_dict()

        permission_modes = []
        for permission_modes_item_data in self.permission_modes:
            permission_modes_item = permission_modes_item_data.to_dict()
            permission_modes.append(permission_modes_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "default_permission": default_permission,
                "permission_modes": permission_modes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tool_permission_mode import ToolPermissionMode
        from ..models.tool_permission_selection import ToolPermissionSelection

        d = dict(src_dict)
        default_permission = ToolPermissionSelection.from_dict(
            d.pop("default_permission")
        )

        permission_modes = []
        _permission_modes = d.pop("permission_modes")
        for permission_modes_item_data in _permission_modes:
            permission_modes_item = ToolPermissionMode.from_dict(
                permission_modes_item_data
            )

            permission_modes.append(permission_modes_item)

        tool_permission_profile = cls(
            default_permission=default_permission,
            permission_modes=permission_modes,
        )

        return tool_permission_profile
