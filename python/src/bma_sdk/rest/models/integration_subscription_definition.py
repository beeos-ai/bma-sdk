from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.integration_subscription_definition_conversation_schema import (
        IntegrationSubscriptionDefinitionConversationSchema,
    )


T = TypeVar("T", bound="IntegrationSubscriptionDefinition")


@_attrs_define
class IntegrationSubscriptionDefinition:
    """
    Attributes:
        conversation_schema (IntegrationSubscriptionDefinitionConversationSchema): Schema for one concrete provider
            conversation address.
    """

    conversation_schema: "IntegrationSubscriptionDefinitionConversationSchema"

    def to_dict(self) -> dict[str, Any]:
        conversation_schema = self.conversation_schema.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "conversation_schema": conversation_schema,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_subscription_definition_conversation_schema import (
            IntegrationSubscriptionDefinitionConversationSchema,
        )

        d = dict(src_dict)
        conversation_schema = (
            IntegrationSubscriptionDefinitionConversationSchema.from_dict(
                d.pop("conversation_schema")
            )
        )

        integration_subscription_definition = cls(
            conversation_schema=conversation_schema,
        )

        return integration_subscription_definition
