from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.event_webhook_model_output_event_event import (
    EventWebhookModelOutputEventEvent,
    check_event_webhook_model_output_event_event,
)

if TYPE_CHECKING:
    from ..models.model_output_event import ModelOutputEvent


T = TypeVar("T", bound="EventWebhookModelOutputEvent")


@_attrs_define
class EventWebhookModelOutputEvent:
    """
    Attributes:
        event (EventWebhookModelOutputEventEvent):
        data (ModelOutputEvent):
    """

    event: EventWebhookModelOutputEventEvent
    data: "ModelOutputEvent"

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
        from ..models.model_output_event import ModelOutputEvent

        d = dict(src_dict)
        event = check_event_webhook_model_output_event_event(d.pop("event"))

        data = ModelOutputEvent.from_dict(d.pop("data"))

        event_webhook_model_output_event = cls(
            event=event,
            data=data,
        )

        return event_webhook_model_output_event
