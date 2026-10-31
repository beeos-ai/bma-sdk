from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.integration_conversation import IntegrationConversation


T = TypeVar("T", bound="CreateIntegrationSubscriptionRequest")


@_attrs_define
class CreateIntegrationSubscriptionRequest:
    """
    Attributes:
        agent_id (str):
        conversation (IntegrationConversation): One concrete provider address, validated by the integration's
            capabilities.subscription.conversation_schema. Slack uses channel_id and optional thread_ts; Discord uses
            channel_id for a channel or thread_id for a thread; GitHub uses repository_id and pull_request. Discord accepts
            optional parent channel_id and guild_id alongside thread_id and validates their ID format, but subscription
            creation does not verify them against Discord or retain them as routing restrictions. Only thread_id is retained
            in a canonical thread address and returned by create/list responses. No credentials or runtime state.
    """

    agent_id: str
    conversation: "IntegrationConversation"

    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        conversation = self.conversation.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "agent_id": agent_id,
                "conversation": conversation,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_conversation import IntegrationConversation

        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        conversation = IntegrationConversation.from_dict(d.pop("conversation"))

        create_integration_subscription_request = cls(
            agent_id=agent_id,
            conversation=conversation,
        )

        return create_integration_subscription_request
