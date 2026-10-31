from typing import Literal, cast

EventWebhookScopeType = Literal["agent", "profile", "project"]

EVENT_WEBHOOK_SCOPE_TYPE_VALUES: set[EventWebhookScopeType] = {
    "agent",
    "profile",
    "project",
}


def check_event_webhook_scope_type(value: str) -> EventWebhookScopeType:
    if value in EVENT_WEBHOOK_SCOPE_TYPE_VALUES:
        return cast(EventWebhookScopeType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {EVENT_WEBHOOK_SCOPE_TYPE_VALUES!r}"
    )
