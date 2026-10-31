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
    from ..models.integration_capability_definition_input_schema import (
        IntegrationCapabilityDefinitionInputSchema,
    )


T = TypeVar("T", bound="IntegrationCapabilityDefinition")


@_attrs_define
class IntegrationCapabilityDefinition:
    """
    Attributes:
        input_schema (IntegrationCapabilityDefinitionInputSchema): Static argument schema for this operation or
            interaction handler. Shipped integration tools accept action arguments and use the conversation assigned at
            launch; execution fails if no conversation is assigned. Shipped interaction handlers use the assigned
            conversation and accept empty arguments.
        description (Union[Unset, str]):
    """

    input_schema: "IntegrationCapabilityDefinitionInputSchema"
    description: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        input_schema = self.input_schema.to_dict()

        description = self.description

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "input_schema": input_schema,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_capability_definition_input_schema import (
            IntegrationCapabilityDefinitionInputSchema,
        )

        d = dict(src_dict)
        input_schema = IntegrationCapabilityDefinitionInputSchema.from_dict(
            d.pop("input_schema")
        )

        description = d.pop("description", UNSET)

        integration_capability_definition = cls(
            input_schema=input_schema,
            description=description,
        )

        return integration_capability_definition
