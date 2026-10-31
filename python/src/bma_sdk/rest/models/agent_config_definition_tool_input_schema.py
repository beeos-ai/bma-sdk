from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config_definition_tool_input_schema_properties import (
        AgentConfigDefinitionToolInputSchemaProperties,
    )


T = TypeVar("T", bound="AgentConfigDefinitionToolInputSchema")


@_attrs_define
class AgentConfigDefinitionToolInputSchema:
    """A JSON Schema for the tool's input. Keywords beyond those listed, such as additionalProperties or description, are
    allowed.

        Attributes:
            type_ (Literal['object']):
            properties (Union[Unset, AgentConfigDefinitionToolInputSchemaProperties]):
            required (Union[Unset, list[str]]):
    """

    type_: Literal["object"]
    properties: Union[Unset, "AgentConfigDefinitionToolInputSchemaProperties"] = UNSET
    required: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        properties: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        required: Union[Unset, list[str]] = UNSET
        if not isinstance(self.required, Unset):
            required = self.required

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if properties is not UNSET:
            field_dict["properties"] = properties
        if required is not UNSET:
            field_dict["required"] = required

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_definition_tool_input_schema_properties import (
            AgentConfigDefinitionToolInputSchemaProperties,
        )

        d = dict(src_dict)
        type_ = cast(Literal["object"], d.pop("type"))
        if type_ != "object":
            raise ValueError(f"type must match const 'object', got '{type_}'")

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, AgentConfigDefinitionToolInputSchemaProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = AgentConfigDefinitionToolInputSchemaProperties.from_dict(
                _properties
            )

        required = cast(list[str], d.pop("required", UNSET))

        agent_config_definition_tool_input_schema = cls(
            type_=type_,
            properties=properties,
            required=required,
        )

        agent_config_definition_tool_input_schema.additional_properties = d
        return agent_config_definition_tool_input_schema

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
