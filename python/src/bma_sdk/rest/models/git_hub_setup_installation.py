from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="GitHubSetupInstallation")


@_attrs_define
class GitHubSetupInstallation:
    """
    Attributes:
        id (str):
        account (str): Provider-verified installation account login.
        settings_url (str):
        account_type (Union[Unset, str]):
    """

    id: str
    account: str
    settings_url: str
    account_type: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        account = self.account

        settings_url = self.settings_url

        account_type = self.account_type

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "account": account,
                "settings_url": settings_url,
            }
        )
        if account_type is not UNSET:
            field_dict["account_type"] = account_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        account = d.pop("account")

        settings_url = d.pop("settings_url")

        account_type = d.pop("account_type", UNSET)

        git_hub_setup_installation = cls(
            id=id,
            account=account,
            settings_url=settings_url,
            account_type=account_type,
        )

        return git_hub_setup_installation
