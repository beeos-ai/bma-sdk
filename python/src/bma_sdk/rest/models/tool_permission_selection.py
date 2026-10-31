from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.tool_permission_selection_parameters import (
        ToolPermissionSelectionParameters,
    )


T = TypeVar("T", bound="ToolPermissionSelection")


@_attrs_define
class ToolPermissionSelection:
    """
    Attributes:
        mode (str):
        parameters (ToolPermissionSelectionParameters):
    """

    mode: str
    parameters: "ToolPermissionSelectionParameters"

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode

        parameters = self.parameters.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "mode": mode,
                "parameters": parameters,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tool_permission_selection_parameters import (
            ToolPermissionSelectionParameters,
        )

        d = dict(src_dict)
        mode = d.pop("mode")

        parameters = ToolPermissionSelectionParameters.from_dict(d.pop("parameters"))

        tool_permission_selection = cls(
            mode=mode,
            parameters=parameters,
        )

        return tool_permission_selection
