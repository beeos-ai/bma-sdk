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
    from ..models.tool_permission_mode import ToolPermissionMode
    from ..models.tool_permission_selection import ToolPermissionSelection


T = TypeVar("T", bound="ToolCatalogEntry")


@_attrs_define
class ToolCatalogEntry:
    """
    Attributes:
        name (str):
        description (str):
        default_permission (ToolPermissionSelection):
        permission_modes (list['ToolPermissionMode']):
        implicit (Union[Unset, bool]): Whether this tool supports implicit inclusion based on config resources or
            integration context, even when explicitly configured.
    """

    name: str
    description: str
    default_permission: "ToolPermissionSelection"
    permission_modes: list["ToolPermissionMode"]
    implicit: Union[Unset, bool] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        default_permission = self.default_permission.to_dict()

        permission_modes = []
        for permission_modes_item_data in self.permission_modes:
            permission_modes_item = permission_modes_item_data.to_dict()
            permission_modes.append(permission_modes_item)

        implicit = self.implicit

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "description": description,
                "default_permission": default_permission,
                "permission_modes": permission_modes,
            }
        )
        if implicit is not UNSET:
            field_dict["implicit"] = implicit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tool_permission_mode import ToolPermissionMode
        from ..models.tool_permission_selection import ToolPermissionSelection

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

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

        implicit = d.pop("implicit", UNSET)

        tool_catalog_entry = cls(
            name=name,
            description=description,
            default_permission=default_permission,
            permission_modes=permission_modes,
            implicit=implicit,
        )

        return tool_catalog_entry
