from typing import Literal, cast

AgentProfileEventWebhookScopeType = Literal["profile"]

AGENT_PROFILE_EVENT_WEBHOOK_SCOPE_TYPE_VALUES: set[
    AgentProfileEventWebhookScopeType
] = {
    "profile",
}


def check_agent_profile_event_webhook_scope_type(
    value: str,
) -> AgentProfileEventWebhookScopeType:
    if value in AGENT_PROFILE_EVENT_WEBHOOK_SCOPE_TYPE_VALUES:
        return cast(AgentProfileEventWebhookScopeType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_PROFILE_EVENT_WEBHOOK_SCOPE_TYPE_VALUES!r}"
    )
