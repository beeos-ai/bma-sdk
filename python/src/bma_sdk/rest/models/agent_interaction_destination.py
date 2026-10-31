from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.integration_kind import IntegrationKind, check_integration_kind

if TYPE_CHECKING:
    from ..models.integration_conversation import IntegrationConversation


T = TypeVar("T", bound="AgentInteractionDestination")


@_attrs_define
class AgentInteractionDestination:
    """Immutable handler and destination captured when the interaction was created. Provider delivery and callbacks check
    current integration and handler authority. Dashboard/API resolution remains available independently.

        Attributes:
            integration_kind (IntegrationKind): Registered integration implementation; independent of the saved
                integration's name and immutable ID.
            handler_key (str):
            integration_id (str):
            integration_target_id (str):
            conversation (IntegrationConversation): One concrete provider address, validated by the integration's
                capabilities.subscription.conversation_schema. Slack uses channel_id and optional thread_ts; Discord uses
                channel_id for a channel or thread_id for a thread; GitHub uses repository_id and pull_request. Discord accepts
                optional parent channel_id and guild_id alongside thread_id and validates their ID format, but subscription
                creation does not verify them against Discord or retain them as routing restrictions. Only thread_id is retained
                in a canonical thread address and returned by create/list responses. No credentials or runtime state.
    """

    integration_kind: IntegrationKind
    handler_key: str
    integration_id: str
    integration_target_id: str
    conversation: "IntegrationConversation"

    def to_dict(self) -> dict[str, Any]:
        integration_kind: str = self.integration_kind

        handler_key = self.handler_key

        integration_id = self.integration_id

        integration_target_id = self.integration_target_id

        conversation = self.conversation.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "integration_kind": integration_kind,
                "handler_key": handler_key,
                "integration_id": integration_id,
                "integration_target_id": integration_target_id,
                "conversation": conversation,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_conversation import IntegrationConversation

        d = dict(src_dict)
        integration_kind = check_integration_kind(d.pop("integration_kind"))

        handler_key = d.pop("handler_key")

        integration_id = d.pop("integration_id")

        integration_target_id = d.pop("integration_target_id")

        conversation = IntegrationConversation.from_dict(d.pop("conversation"))

        agent_interaction_destination = cls(
            integration_kind=integration_kind,
            handler_key=handler_key,
            integration_id=integration_id,
            integration_target_id=integration_target_id,
            conversation=conversation,
        )

        return agent_interaction_destination
