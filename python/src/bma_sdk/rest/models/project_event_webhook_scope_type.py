from typing import Literal, cast

ProjectEventWebhookScopeType = Literal["project"]

PROJECT_EVENT_WEBHOOK_SCOPE_TYPE_VALUES: set[ProjectEventWebhookScopeType] = {
    "project",
}


def check_project_event_webhook_scope_type(value: str) -> ProjectEventWebhookScopeType:
    if value in PROJECT_EVENT_WEBHOOK_SCOPE_TYPE_VALUES:
        return cast(ProjectEventWebhookScopeType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROJECT_EVENT_WEBHOOK_SCOPE_TYPE_VALUES!r}"
    )
