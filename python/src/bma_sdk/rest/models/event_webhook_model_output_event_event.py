from typing import Literal, cast

EventWebhookModelOutputEventEvent = Literal["model_output"]

EVENT_WEBHOOK_MODEL_OUTPUT_EVENT_EVENT_VALUES: set[
    EventWebhookModelOutputEventEvent
] = {
    "model_output",
}


def check_event_webhook_model_output_event_event(
    value: str,
) -> EventWebhookModelOutputEventEvent:
    if value in EVENT_WEBHOOK_MODEL_OUTPUT_EVENT_EVENT_VALUES:
        return cast(EventWebhookModelOutputEventEvent, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_WEBHOOK_MODEL_OUTPUT_EVENT_EVENT_VALUES!r}"
    )
