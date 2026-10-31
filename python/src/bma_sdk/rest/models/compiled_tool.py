from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.compiled_tool_type import CompiledToolType, check_compiled_tool_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.compiled_tool_input_schema import CompiledToolInputSchema
    from ..models.tool_permission_selection import ToolPermissionSelection


T = TypeVar("T", bound="CompiledTool")


@_attrs_define
class CompiledTool:
    """
    Attributes:
        enabled (bool):
        permission (ToolPermissionSelection):
        integration_id (Union[Unset, str]):
        type_ (Union[Unset, CompiledToolType]):
        deferred (Union[Unset, bool]):
        description (Union[Unset, str]):
        input_schema (Union[Unset, CompiledToolInputSchema]):
    """

    enabled: bool
    permission: "ToolPermissionSelection"
    integration_id: Union[Unset, str] = UNSET
    type_: Union[Unset, CompiledToolType] = UNSET
    deferred: Union[Unset, bool] = UNSET
    description: Union[Unset, str] = UNSET
    input_schema: Union[Unset, "CompiledToolInputSchema"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        permission = self.permission.to_dict()

        integration_id = self.integration_id

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_

        deferred = self.deferred

        description = self.description

        input_schema: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.input_schema, Unset):
            input_schema = self.input_schema.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "enabled": enabled,
                "permission": permission,
            }
        )
        if integration_id is not UNSET:
            field_dict["integration_id"] = integration_id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if deferred is not UNSET:
            field_dict["deferred"] = deferred
        if description is not UNSET:
            field_dict["description"] = description
        if input_schema is not UNSET:
            field_dict["input_schema"] = input_schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.compiled_tool_input_schema import CompiledToolInputSchema
        from ..models.tool_permission_selection import ToolPermissionSelection

        d = dict(src_dict)
        enabled = d.pop("enabled")

        permission = ToolPermissionSelection.from_dict(d.pop("permission"))

        integration_id = d.pop("integration_id", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, CompiledToolType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = check_compiled_tool_type(_type_)

        deferred = d.pop("deferred", UNSET)

        description = d.pop("description", UNSET)

        _input_schema = d.pop("input_schema", UNSET)
        input_schema: Union[Unset, CompiledToolInputSchema]
        if isinstance(_input_schema, Unset):
            input_schema = UNSET
        else:
            input_schema = CompiledToolInputSchema.from_dict(_input_schema)

        compiled_tool = cls(
            enabled=enabled,
            permission=permission,
            integration_id=integration_id,
            type_=type_,
            deferred=deferred,
            description=description,
            input_schema=input_schema,
        )

        return compiled_tool
