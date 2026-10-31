from typing import Literal, cast

EventWebhookToolCallUpdateEvent = Literal["tool_call_update"]

EVENT_WEBHOOK_TOOL_CALL_UPDATE_EVENT_VALUES: set[EventWebhookToolCallUpdateEvent] = {
    "tool_call_update",
}


def check_event_webhook_tool_call_update_event(
    value: str,
) -> EventWebhookToolCallUpdateEvent:
    if value in EVENT_WEBHOOK_TOOL_CALL_UPDATE_EVENT_VALUES:
        return cast(EventWebhookToolCallUpdateEvent, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_WEBHOOK_TOOL_CALL_UPDATE_EVENT_VALUES!r}"
    )
