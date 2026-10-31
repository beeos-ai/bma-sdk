from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.event_webhook_agent_input_event_event import (
    EventWebhookAgentInputEventEvent,
    check_event_webhook_agent_input_event_event,
)

if TYPE_CHECKING:
    from ..models.agent_input_event import AgentInputEvent


T = TypeVar("T", bound="EventWebhookAgentInputEvent")


@_attrs_define
class EventWebhookAgentInputEvent:
    """
    Attributes:
        event (EventWebhookAgentInputEventEvent):
        data (AgentInputEvent):
    """

    event: EventWebhookAgentInputEventEvent
    data: "AgentInputEvent"

    def to_dict(self) -> dict[str, Any]:
        event: str = self.event

        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "event": event,
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_input_event import AgentInputEvent

        d = dict(src_dict)
        event = check_event_webhook_agent_input_event_event(d.pop("event"))

        data = AgentInputEvent.from_dict(d.pop("data"))

        event_webhook_agent_input_event = cls(
            event=event,
            data=data,
        )

        return event_webhook_agent_input_event
