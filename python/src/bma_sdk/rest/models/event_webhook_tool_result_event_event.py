from typing import Literal, cast

EventWebhookToolResultEventEvent = Literal["tool_result"]

EVENT_WEBHOOK_TOOL_RESULT_EVENT_EVENT_VALUES: set[EventWebhookToolResultEventEvent] = {
    "tool_result",
}


def check_event_webhook_tool_result_event_event(
    value: str,
) -> EventWebhookToolResultEventEvent:
    if value in EVENT_WEBHOOK_TOOL_RESULT_EVENT_EVENT_VALUES:
        return cast(EventWebhookToolResultEventEvent, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_WEBHOOK_TOOL_RESULT_EVENT_EVENT_VALUES!r}"
    )
