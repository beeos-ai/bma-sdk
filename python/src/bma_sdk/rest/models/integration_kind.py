from typing import Literal, cast

IntegrationKind = Literal["discord_thread", "github_pr", "slack_thread"]

INTEGRATION_KIND_VALUES: set[IntegrationKind] = {
    "discord_thread",
    "github_pr",
    "slack_thread",
}


def check_integration_kind(value: str) -> IntegrationKind:
    if value in INTEGRATION_KIND_VALUES:
        return cast(IntegrationKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {INTEGRATION_KIND_VALUES!r}"
    )
