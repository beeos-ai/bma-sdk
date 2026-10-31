from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.event_webhook_tool_result_event_event import (
    EventWebhookToolResultEventEvent,
    check_event_webhook_tool_result_event_event,
)

if TYPE_CHECKING:
    from ..models.tool_result_event import ToolResultEvent


T = TypeVar("T", bound="EventWebhookToolResultEvent")


@_attrs_define
class EventWebhookToolResultEvent:
    """
    Attributes:
        event (EventWebhookToolResultEventEvent):
        data (ToolResultEvent):
    """

    event: EventWebhookToolResultEventEvent
    data: "ToolResultEvent"

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
        from ..models.tool_result_event import ToolResultEvent

        d = dict(src_dict)
        event = check_event_webhook_tool_result_event_event(d.pop("event"))

        data = ToolResultEvent.from_dict(d.pop("data"))

        event_webhook_tool_result_event = cls(
            event=event,
            data=data,
        )

        return event_webhook_tool_result_event
