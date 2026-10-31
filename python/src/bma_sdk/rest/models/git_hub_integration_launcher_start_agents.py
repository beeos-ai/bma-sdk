from typing import Literal, cast

GitHubIntegrationLauncherStartAgents = Literal["both", "mention", "pull_request_opened"]

GIT_HUB_INTEGRATION_LAUNCHER_START_AGENTS_VALUES: set[
    GitHubIntegrationLauncherStartAgents
] = {
    "both",
    "mention",
    "pull_request_opened",
}


def check_git_hub_integration_launcher_start_agents(
    value: str,
) -> GitHubIntegrationLauncherStartAgents:
    if value in GIT_HUB_INTEGRATION_LAUNCHER_START_AGENTS_VALUES:
        return cast(GitHubIntegrationLauncherStartAgents, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GIT_HUB_INTEGRATION_LAUNCHER_START_AGENTS_VALUES!r}"
    )
