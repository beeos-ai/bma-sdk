import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.integration_conversation import IntegrationConversation


T = TypeVar("T", bound="IntegrationSubscription")


@_attrs_define
class IntegrationSubscription:
    """
    Attributes:
        id (str):
        project_id (str): Project ID (proj_...).
        integration_id (str):
        agent_id (str):
        agent_name (str): Agent name. Empty means the agent is unnamed; non-empty values use the ResourceName policy.
        conversation (IntegrationConversation): One concrete provider address, validated by the integration's
            capabilities.subscription.conversation_schema. Slack uses channel_id and optional thread_ts; Discord uses
            channel_id for a channel or thread_id for a thread; GitHub uses repository_id and pull_request. Discord accepts
            optional parent channel_id and guild_id alongside thread_id and validates their ID format, but subscription
            creation does not verify them against Discord or retain them as routing restrictions. Only thread_id is retained
            in a canonical thread address and returned by create/list responses. No credentials or runtime state.
        created_at (datetime.datetime):
        conversation_name (Union[Unset, str]): Saved display name for the conversation, when available.
    """

    id: str
    project_id: str
    integration_id: str
    agent_id: str
    agent_name: str
    conversation: "IntegrationConversation"
    created_at: datetime.datetime
    conversation_name: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        project_id = self.project_id

        integration_id = self.integration_id

        agent_id = self.agent_id

        agent_name = self.agent_name

        conversation = self.conversation.to_dict()

        created_at = self.created_at.isoformat()

        conversation_name = self.conversation_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
                "integration_id": integration_id,
                "agent_id": agent_id,
                "agent_name": agent_name,
                "conversation": conversation,
                "created_at": created_at,
            }
        )
        if conversation_name is not UNSET:
            field_dict["conversation_name"] = conversation_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_conversation import IntegrationConversation

        d = dict(src_dict)
        id = d.pop("id")

        project_id = d.pop("project_id")

        integration_id = d.pop("integration_id")

        agent_id = d.pop("agent_id")

        agent_name = d.pop("agent_name")

        conversation = IntegrationConversation.from_dict(d.pop("conversation"))

        created_at = isoparse(d.pop("created_at"))

        conversation_name = d.pop("conversation_name", UNSET)

        integration_subscription = cls(
            id=id,
            project_id=project_id,
            integration_id=integration_id,
            agent_id=agent_id,
            agent_name=agent_name,
            conversation=conversation,
            created_at=created_at,
            conversation_name=conversation_name,
        )

        return integration_subscription
