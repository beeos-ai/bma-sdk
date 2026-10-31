from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.event_webhook_tool_call_update_event import (
    EventWebhookToolCallUpdateEvent,
    check_event_webhook_tool_call_update_event,
)

if TYPE_CHECKING:
    from ..models.tool_call_update import ToolCallUpdate


T = TypeVar("T", bound="EventWebhookToolCallUpdate")


@_attrs_define
class EventWebhookToolCallUpdate:
    """
    Attributes:
        event (EventWebhookToolCallUpdateEvent):
        data (ToolCallUpdate): A notification that a tool call entered a lifecycle state. On the event stream, this is
            ephemeral and sent for the streamed agent and every subagent beneath it, so questions, permission requests, and
            custom tool calls anywhere in the tree surface here; query the list endpoints with `include_subagents` for the
            current rows.
    """

    event: EventWebhookToolCallUpdateEvent
    data: "ToolCallUpdate"

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
        from ..models.tool_call_update import ToolCallUpdate

        d = dict(src_dict)
        event = check_event_webhook_tool_call_update_event(d.pop("event"))

        data = ToolCallUpdate.from_dict(d.pop("data"))

        event_webhook_tool_call_update = cls(
            event=event,
            data=data,
        )

        return event_webhook_tool_call_update
