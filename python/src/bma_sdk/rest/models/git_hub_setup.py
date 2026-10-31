import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.git_hub_setup_manifest import GitHubSetupManifest


T = TypeVar("T", bound="GitHubSetup")


@_attrs_define
class GitHubSetup:
    """
    Attributes:
        integration_id (str):
        setup_revision (int):
        registration_url (str):
        manifest (GitHubSetupManifest): Server-authored GitHub App manifest. Serialize this object to the manifest form
            field when posting to registration_url.
        expires_at (datetime.datetime):
    """

    integration_id: str
    setup_revision: int
    registration_url: str
    manifest: "GitHubSetupManifest"
    expires_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        integration_id = self.integration_id

        setup_revision = self.setup_revision

        registration_url = self.registration_url

        manifest = self.manifest.to_dict()

        expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "integration_id": integration_id,
                "setup_revision": setup_revision,
                "registration_url": registration_url,
                "manifest": manifest,
                "expires_at": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.git_hub_setup_manifest import GitHubSetupManifest

        d = dict(src_dict)
        integration_id = d.pop("integration_id")

        setup_revision = d.pop("setup_revision")

        registration_url = d.pop("registration_url")

        manifest = GitHubSetupManifest.from_dict(d.pop("manifest"))

        expires_at = isoparse(d.pop("expires_at"))

        git_hub_setup = cls(
            integration_id=integration_id,
            setup_revision=setup_revision,
            registration_url=registration_url,
            manifest=manifest,
            expires_at=expires_at,
        )

        return git_hub_setup
