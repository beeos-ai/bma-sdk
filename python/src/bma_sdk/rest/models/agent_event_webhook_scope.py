from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.agent_event_webhook_scope_type import (
    AgentEventWebhookScopeType,
    check_agent_event_webhook_scope_type,
)

T = TypeVar("T", bound="AgentEventWebhookScope")


@_attrs_define
class AgentEventWebhookScope:
    """Watches only this agent, not its descendants.

    Attributes:
        type_ (AgentEventWebhookScopeType):
        agent_id (str):
    """

    type_: AgentEventWebhookScopeType
    agent_id: str

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        agent_id = self.agent_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "agent_id": agent_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_agent_event_webhook_scope_type(d.pop("type"))

        agent_id = d.pop("agent_id")

        agent_event_webhook_scope = cls(
            type_=type_,
            agent_id=agent_id,
        )

        return agent_event_webhook_scope
