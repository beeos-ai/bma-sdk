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
    from ..models.integration_conversation import IntegrationConversation


T = TypeVar("T", bound="IntegrationTarget")


@_attrs_define
class IntegrationTarget:
    """
    Attributes:
        provider (str):
        conversation (IntegrationConversation): One concrete provider address, validated by the integration's
            capabilities.subscription.conversation_schema. Slack uses channel_id and optional thread_ts; Discord uses
            channel_id for a channel or thread_id for a thread; GitHub uses repository_id and pull_request. Discord accepts
            optional parent channel_id and guild_id alongside thread_id and validates their ID format, but subscription
            creation does not verify them against Discord or retain them as routing restrictions. Only thread_id is retained
            in a canonical thread address and returned by create/list responses. No credentials or runtime state.
        display_name (str):
        provider_uri (Union[Unset, str]):
    """

    provider: str
    conversation: "IntegrationConversation"
    display_name: str
    provider_uri: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        provider = self.provider

        conversation = self.conversation.to_dict()

        display_name = self.display_name

        provider_uri = self.provider_uri

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "provider": provider,
                "conversation": conversation,
                "display_name": display_name,
            }
        )
        if provider_uri is not UNSET:
            field_dict["provider_uri"] = provider_uri

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_conversation import IntegrationConversation

        d = dict(src_dict)
        provider = d.pop("provider")

        conversation = IntegrationConversation.from_dict(d.pop("conversation"))

        display_name = d.pop("display_name")

        provider_uri = d.pop("provider_uri", UNSET)

        integration_target = cls(
            provider=provider,
            conversation=conversation,
            display_name=display_name,
            provider_uri=provider_uri,
        )

        return integration_target
