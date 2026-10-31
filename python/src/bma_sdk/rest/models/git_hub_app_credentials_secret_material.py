from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.git_hub_app_credentials_secret_material_kind import (
    GitHubAppCredentialsSecretMaterialKind,
    check_git_hub_app_credentials_secret_material_kind,
)

T = TypeVar("T", bound="GitHubAppCredentialsSecretMaterial")


@_attrs_define
class GitHubAppCredentialsSecretMaterial:
    """
    Attributes:
        kind (GitHubAppCredentialsSecretMaterialKind):
        app_id (str):
        private_key (str): Unencrypted RSA private key in PEM format. Stored encrypted.
        webhook_secret (str):
    """

    kind: GitHubAppCredentialsSecretMaterialKind
    app_id: str
    private_key: str
    webhook_secret: str

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        app_id = self.app_id

        private_key = self.private_key

        webhook_secret = self.webhook_secret

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "app_id": app_id,
                "private_key": private_key,
                "webhook_secret": webhook_secret,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_git_hub_app_credentials_secret_material_kind(d.pop("kind"))

        app_id = d.pop("app_id")

        private_key = d.pop("private_key")

        webhook_secret = d.pop("webhook_secret")

        git_hub_app_credentials_secret_material = cls(
            kind=kind,
            app_id=app_id,
            private_key=private_key,
            webhook_secret=webhook_secret,
        )

        return git_hub_app_credentials_secret_material
