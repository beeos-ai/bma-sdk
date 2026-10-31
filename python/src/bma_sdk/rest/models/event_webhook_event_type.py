from typing import Literal, cast

EventWebhookEventType = Literal[
    "agent_input",
    "context_checkpoint",
    "model_output",
    "tool_call_update",
    "tool_result",
]

EVENT_WEBHOOK_EVENT_TYPE_VALUES: set[EventWebhookEventType] = {
    "agent_input",
    "context_checkpoint",
    "model_output",
    "tool_call_update",
    "tool_result",
}


def check_event_webhook_event_type(value: str) -> EventWebhookEventType:
    if value in EVENT_WEBHOOK_EVENT_TYPE_VALUES:
        return cast(EventWebhookEventType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_WEBHOOK_EVENT_TYPE_VALUES!r}"
    )
