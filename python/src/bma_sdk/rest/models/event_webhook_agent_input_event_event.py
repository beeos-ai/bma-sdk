from typing import Literal, cast

EventWebhookAgentInputEventEvent = Literal["agent_input"]

EVENT_WEBHOOK_AGENT_INPUT_EVENT_EVENT_VALUES: set[EventWebhookAgentInputEventEvent] = {
    "agent_input",
}


def check_event_webhook_agent_input_event_event(
    value: str,
) -> EventWebhookAgentInputEventEvent:
    if value in EVENT_WEBHOOK_AGENT_INPUT_EVENT_EVENT_VALUES:
        return cast(EventWebhookAgentInputEventEvent, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_WEBHOOK_AGENT_INPUT_EVENT_EVENT_VALUES!r}"
    )
