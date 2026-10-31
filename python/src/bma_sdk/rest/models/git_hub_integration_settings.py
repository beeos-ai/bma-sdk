from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.git_hub_integration_launcher import GitHubIntegrationLauncher


T = TypeVar("T", bound="GitHubIntegrationSettings")


@_attrs_define
class GitHubIntegrationSettings:
    """
    Attributes:
        launcher (Union[Unset, GitHubIntegrationLauncher]):
        code_write (Union[Unset, bool]): Git credentials can push. Off by default: read-only.
    """

    launcher: Union[Unset, "GitHubIntegrationLauncher"] = UNSET
    code_write: Union[Unset, bool] = UNSET

    def to_dict(self) -> dict[str, Any]:
        launcher: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.launcher, Unset):
            launcher = self.launcher.to_dict()

        code_write = self.code_write

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if launcher is not UNSET:
            field_dict["launcher"] = launcher
        if code_write is not UNSET:
            field_dict["code_write"] = code_write

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.git_hub_integration_launcher import GitHubIntegrationLauncher

        d = dict(src_dict)
        _launcher = d.pop("launcher", UNSET)
        launcher: Union[Unset, GitHubIntegrationLauncher]
        if isinstance(_launcher, Unset):
            launcher = UNSET
        else:
            launcher = GitHubIntegrationLauncher.from_dict(_launcher)

        code_write = d.pop("code_write", UNSET)

        git_hub_integration_settings = cls(
            launcher=launcher,
            code_write=code_write,
        )

        return git_hub_integration_settings
