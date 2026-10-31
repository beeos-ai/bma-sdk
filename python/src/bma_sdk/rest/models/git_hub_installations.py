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
    from ..models.git_hub_setup_installation import GitHubSetupInstallation


T = TypeVar("T", bound="GitHubInstallations")


@_attrs_define
class GitHubInstallations:
    """
    Attributes:
        provider_app_id (str):
        name (str):
        slug (str):
        install_url (str): Verified GitHub App installation URL. Its state may carry the public credential secret ID as
            a recovery hint, never credentials or authorization.
        installations (list['GitHubSetupInstallation']):
        next_page (Union[Unset, int]):
    """

    provider_app_id: str
    name: str
    slug: str
    install_url: str
    installations: list["GitHubSetupInstallation"]
    next_page: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        provider_app_id = self.provider_app_id

        name = self.name

        slug = self.slug

        install_url = self.install_url

        installations = []
        for installations_item_data in self.installations:
            installations_item = installations_item_data.to_dict()
            installations.append(installations_item)

        next_page = self.next_page

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "provider_app_id": provider_app_id,
                "name": name,
                "slug": slug,
                "install_url": install_url,
                "installations": installations,
            }
        )
        if next_page is not UNSET:
            field_dict["next_page"] = next_page

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.git_hub_setup_installation import GitHubSetupInstallation

        d = dict(src_dict)
        provider_app_id = d.pop("provider_app_id")

        name = d.pop("name")

        slug = d.pop("slug")

        install_url = d.pop("install_url")

        installations = []
        _installations = d.pop("installations")
        for installations_item_data in _installations:
            installations_item = GitHubSetupInstallation.from_dict(
                installations_item_data
            )

            installations.append(installations_item)

        next_page = d.pop("next_page", UNSET)

        git_hub_installations = cls(
            provider_app_id=provider_app_id,
            name=name,
            slug=slug,
            install_url=install_url,
            installations=installations,
            next_page=next_page,
        )

        return git_hub_installations
