from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.git_hub_integration_launcher_start_agents import (
    GitHubIntegrationLauncherStartAgents,
    check_git_hub_integration_launcher_start_agents,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="GitHubIntegrationLauncher")


@_attrs_define
class GitHubIntegrationLauncher:
    """
    Attributes:
        profile (str):
        trigger (GitHubIntegrationLauncherStartAgents):
        repository_id (Union[Unset, str]): Optional: restrict launches to this repository.
    """

    profile: str
    trigger: GitHubIntegrationLauncherStartAgents
    repository_id: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        profile = self.profile

        trigger: str = self.trigger

        repository_id = self.repository_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "profile": profile,
                "trigger": trigger,
            }
        )
        if repository_id is not UNSET:
            field_dict["repository_id"] = repository_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        profile = d.pop("profile")

        trigger = check_git_hub_integration_launcher_start_agents(d.pop("trigger"))

        repository_id = d.pop("repository_id", UNSET)

        git_hub_integration_launcher = cls(
            profile=profile,
            trigger=trigger,
            repository_id=repository_id,
        )

        return git_hub_integration_launcher
