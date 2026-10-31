from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.tool_permission_mode_parameters_schema import (
        ToolPermissionModeParametersSchema,
    )


T = TypeVar("T", bound="ToolPermissionMode")


@_attrs_define
class ToolPermissionMode:
    """
    Attributes:
        name (str):
        label (str):
        description (str):
        parameters_schema (ToolPermissionModeParametersSchema):
    """

    name: str
    label: str
    description: str
    parameters_schema: "ToolPermissionModeParametersSchema"

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        label = self.label

        description = self.description

        parameters_schema = self.parameters_schema.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "label": label,
                "description": description,
                "parameters_schema": parameters_schema,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tool_permission_mode_parameters_schema import (
            ToolPermissionModeParametersSchema,
        )

        d = dict(src_dict)
        name = d.pop("name")

        label = d.pop("label")

        description = d.pop("description")

        parameters_schema = ToolPermissionModeParametersSchema.from_dict(
            d.pop("parameters_schema")
        )

        tool_permission_mode = cls(
            name=name,
            label=label,
            description=description,
            parameters_schema=parameters_schema,
        )

        return tool_permission_mode
