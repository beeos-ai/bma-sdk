from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.aws_credentials_secret_material import AWSCredentialsSecretMaterial
    from ..models.generic_secret_material import GenericSecretMaterial
    from ..models.git_hub_app_credentials_secret_material import (
        GitHubAppCredentialsSecretMaterial,
    )
    from ..models.o_auth_token_set_secret_material import OAuthTokenSetSecretMaterial


T = TypeVar("T", bound="SecretVersionRequest")


@_attrs_define
class SecretVersionRequest:
    """
    Attributes:
        material (Union['AWSCredentialsSecretMaterial', 'GenericSecretMaterial', 'GitHubAppCredentialsSecretMaterial',
            'OAuthTokenSetSecretMaterial']): The secret's value. kind selects its shape: generic, oauth_token_set,
            aws_credentials, or github_app_credentials.
    """

    material: Union[
        "AWSCredentialsSecretMaterial",
        "GenericSecretMaterial",
        "GitHubAppCredentialsSecretMaterial",
        "OAuthTokenSetSecretMaterial",
    ]

    def to_dict(self) -> dict[str, Any]:
        from ..models.aws_credentials_secret_material import (
            AWSCredentialsSecretMaterial,
        )
        from ..models.generic_secret_material import GenericSecretMaterial
        from ..models.o_auth_token_set_secret_material import (
            OAuthTokenSetSecretMaterial,
        )

        material: dict[str, Any]
        if isinstance(self.material, GenericSecretMaterial):
            material = self.material.to_dict()
        elif isinstance(self.material, OAuthTokenSetSecretMaterial):
            material = self.material.to_dict()
        elif isinstance(self.material, AWSCredentialsSecretMaterial):
            material = self.material.to_dict()
        else:
            material = self.material.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "material": material,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aws_credentials_secret_material import (
            AWSCredentialsSecretMaterial,
        )
        from ..models.generic_secret_material import GenericSecretMaterial
        from ..models.git_hub_app_credentials_secret_material import (
            GitHubAppCredentialsSecretMaterial,
        )
        from ..models.o_auth_token_set_secret_material import (
            OAuthTokenSetSecretMaterial,
        )

        d = dict(src_dict)

        def _parse_material(
            data: object,
        ) -> Union[
            "AWSCredentialsSecretMaterial",
            "GenericSecretMaterial",
            "GitHubAppCredentialsSecretMaterial",
            "OAuthTokenSetSecretMaterial",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_secret_material_type_0 = (
                    GenericSecretMaterial.from_dict(data)
                )

                return componentsschemas_secret_material_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_secret_material_type_1 = (
                    OAuthTokenSetSecretMaterial.from_dict(data)
                )

                return componentsschemas_secret_material_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_secret_material_type_2 = (
                    AWSCredentialsSecretMaterial.from_dict(data)
                )

                return componentsschemas_secret_material_type_2
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_secret_material_type_3 = (
                GitHubAppCredentialsSecretMaterial.from_dict(data)
            )

            return componentsschemas_secret_material_type_3

        material = _parse_material(d.pop("material"))

        secret_version_request = cls(
            material=material,
        )

        return secret_version_request
