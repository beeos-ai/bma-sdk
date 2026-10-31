from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..models.agent_config_definition_tool_type import (
    AgentConfigDefinitionToolType,
    check_agent_config_definition_tool_type,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config_definition_tool_input_schema import (
        AgentConfigDefinitionToolInputSchema,
    )
    from ..models.agent_config_definition_tool_permission import (
        AgentConfigDefinitionToolPermission,
    )


T = TypeVar("T", bound="AgentConfigDefinitionTool")


@_attrs_define
class AgentConfigDefinitionTool:
    """
    Attributes:
        deferred (Union[Unset, bool]):
        description (Union[Unset, str]):
        enabled (Union[None, Unset, bool]):
        input_schema (Union[Unset, AgentConfigDefinitionToolInputSchema]): A JSON Schema for the tool's input. Keywords
            beyond those listed, such as additionalProperties or description, are allowed.
        permission (Union[Unset, AgentConfigDefinitionToolPermission]):
        type_ (Union[Unset, AgentConfigDefinitionToolType]):
    """

    deferred: Union[Unset, bool] = UNSET
    description: Union[Unset, str] = UNSET
    enabled: Union[None, Unset, bool] = UNSET
    input_schema: Union[Unset, "AgentConfigDefinitionToolInputSchema"] = UNSET
    permission: Union[Unset, "AgentConfigDefinitionToolPermission"] = UNSET
    type_: Union[Unset, AgentConfigDefinitionToolType] = UNSET

    def to_dict(self) -> dict[str, Any]:
        deferred = self.deferred

        description = self.description

        enabled: Union[None, Unset, bool]
        if isinstance(self.enabled, Unset):
            enabled = UNSET
        else:
            enabled = self.enabled

        input_schema: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.input_schema, Unset):
            input_schema = self.input_schema.to_dict()

        permission: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.permission, Unset):
            permission = self.permission.to_dict()

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if deferred is not UNSET:
            field_dict["deferred"] = deferred
        if description is not UNSET:
            field_dict["description"] = description
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if input_schema is not UNSET:
            field_dict["input_schema"] = input_schema
        if permission is not UNSET:
            field_dict["permission"] = permission
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_definition_tool_input_schema import (
            AgentConfigDefinitionToolInputSchema,
        )
        from ..models.agent_config_definition_tool_permission import (
            AgentConfigDefinitionToolPermission,
        )

        d = dict(src_dict)
        deferred = d.pop("deferred", UNSET)

        description = d.pop("description", UNSET)

        def _parse_enabled(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        enabled = _parse_enabled(d.pop("enabled", UNSET))

        _input_schema = d.pop("input_schema", UNSET)
        input_schema: Union[Unset, AgentConfigDefinitionToolInputSchema]
        if isinstance(_input_schema, Unset):
            input_schema = UNSET
        else:
            input_schema = AgentConfigDefinitionToolInputSchema.from_dict(_input_schema)

        _permission = d.pop("permission", UNSET)
        permission: Union[Unset, AgentConfigDefinitionToolPermission]
        if isinstance(_permission, Unset):
            permission = UNSET
        else:
            permission = AgentConfigDefinitionToolPermission.from_dict(_permission)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, AgentConfigDefinitionToolType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = check_agent_config_definition_tool_type(_type_)

        agent_config_definition_tool = cls(
            deferred=deferred,
            description=description,
            enabled=enabled,
            input_schema=input_schema,
            permission=permission,
            type_=type_,
        )

        return agent_config_definition_tool
