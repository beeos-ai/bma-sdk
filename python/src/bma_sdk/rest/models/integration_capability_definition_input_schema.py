from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="IntegrationCapabilityDefinitionInputSchema")


@_attrs_define
class IntegrationCapabilityDefinitionInputSchema:
    """Static argument schema for this operation or interaction handler. Shipped integration tools accept action arguments
    and use the conversation assigned at launch; execution fails if no conversation is assigned. Shipped interaction
    handlers use the assigned conversation and accept empty arguments.

    """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        integration_capability_definition_input_schema = cls()

        integration_capability_definition_input_schema.additional_properties = d
        return integration_capability_definition_input_schema

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
