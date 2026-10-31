from typing import Literal, cast

EventWebhookContextCheckpointEventEvent = Literal["context_checkpoint"]

EVENT_WEBHOOK_CONTEXT_CHECKPOINT_EVENT_EVENT_VALUES: set[
    EventWebhookContextCheckpointEventEvent
] = {
    "context_checkpoint",
}


def check_event_webhook_context_checkpoint_event_event(
    value: str,
) -> EventWebhookContextCheckpointEventEvent:
    if value in EVENT_WEBHOOK_CONTEXT_CHECKPOINT_EVENT_EVENT_VALUES:
        return cast(EventWebhookContextCheckpointEventEvent, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_WEBHOOK_CONTEXT_CHECKPOINT_EVENT_EVENT_VALUES!r}"
    )
