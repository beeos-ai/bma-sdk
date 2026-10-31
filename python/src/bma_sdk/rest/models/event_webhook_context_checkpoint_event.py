from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.event_webhook_context_checkpoint_event_event import (
    EventWebhookContextCheckpointEventEvent,
    check_event_webhook_context_checkpoint_event_event,
)

if TYPE_CHECKING:
    from ..models.context_checkpoint_event import ContextCheckpointEvent


T = TypeVar("T", bound="EventWebhookContextCheckpointEvent")


@_attrs_define
class EventWebhookContextCheckpointEvent:
    """
    Attributes:
        event (EventWebhookContextCheckpointEventEvent):
        data (ContextCheckpointEvent):
    """

    event: EventWebhookContextCheckpointEventEvent
    data: "ContextCheckpointEvent"

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
        from ..models.context_checkpoint_event import ContextCheckpointEvent

        d = dict(src_dict)
        event = check_event_webhook_context_checkpoint_event_event(d.pop("event"))

        data = ContextCheckpointEvent.from_dict(d.pop("data"))

        event_webhook_context_checkpoint_event = cls(
            event=event,
            data=data,
        )

        return event_webhook_context_checkpoint_event
