from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateGitHubSetupRequest")


@_attrs_define
class CreateGitHubSetupRequest:
    """
    Attributes:
        expected_setup_revision (int):
        app_name (Union[Unset, str]): Optional initial GitHub App name suggestion. When omitted, the user chooses a name
            on GitHub during registration.
        organization (Union[Unset, str]): GitHub organization login. Omit to register under a personal account.
    """

    expected_setup_revision: int
    app_name: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        expected_setup_revision = self.expected_setup_revision

        app_name = self.app_name

        organization = self.organization

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "expected_setup_revision": expected_setup_revision,
            }
        )
        if app_name is not UNSET:
            field_dict["app_name"] = app_name
        if organization is not UNSET:
            field_dict["organization"] = organization

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        expected_setup_revision = d.pop("expected_setup_revision")

        app_name = d.pop("app_name", UNSET)

        organization = d.pop("organization", UNSET)

        create_git_hub_setup_request = cls(
            expected_setup_revision=expected_setup_revision,
            app_name=app_name,
            organization=organization,
        )

        return create_git_hub_setup_request
