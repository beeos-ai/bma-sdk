from typing import Literal, cast

AgentEventWebhookScopeType = Literal["agent"]

AGENT_EVENT_WEBHOOK_SCOPE_TYPE_VALUES: set[AgentEventWebhookScopeType] = {
    "agent",
}


def check_agent_event_webhook_scope_type(value: str) -> AgentEventWebhookScopeType:
    if value in AGENT_EVENT_WEBHOOK_SCOPE_TYPE_VALUES:
        return cast(AgentEventWebhookScopeType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_EVENT_WEBHOOK_SCOPE_TYPE_VALUES!r}"
    )
