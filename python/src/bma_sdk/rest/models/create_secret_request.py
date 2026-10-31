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
    from ..models.aws_credentials_secret_material import AWSCredentialsSecretMaterial
    from ..models.generic_secret_material import GenericSecretMaterial
    from ..models.git_hub_app_credentials_secret_material import (
        GitHubAppCredentialsSecretMaterial,
    )
    from ..models.metadata import Metadata
    from ..models.o_auth_token_set_secret_material import OAuthTokenSetSecretMaterial
    from ..models.org_secret_owner_input import OrgSecretOwnerInput
    from ..models.project_secret_owner_input import ProjectSecretOwnerInput
    from ..models.user_secret_owner_input import UserSecretOwnerInput


T = TypeVar("T", bound="CreateSecretRequest")


@_attrs_define
class CreateSecretRequest:
    """
    Attributes:
        owner (Union['OrgSecretOwnerInput', 'ProjectSecretOwnerInput', 'UserSecretOwnerInput']): Who owns the secret:
            {"kind":"org"}, {"kind":"project","project_id":"proj_..."}, or {"kind":"user"}. The owner cannot change later.
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        material (Union['AWSCredentialsSecretMaterial', 'GenericSecretMaterial', 'GitHubAppCredentialsSecretMaterial',
            'OAuthTokenSetSecretMaterial']): The secret's value. kind selects its shape: generic, oauth_token_set,
            aws_credentials, or github_app_credentials.
        metadata (Union[Unset, Metadata]): Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64 characters,
            values must be strings of up to 512 characters.
    """

    owner: Union[
        "OrgSecretOwnerInput", "ProjectSecretOwnerInput", "UserSecretOwnerInput"
    ]
    name: str
    material: Union[
        "AWSCredentialsSecretMaterial",
        "GenericSecretMaterial",
        "GitHubAppCredentialsSecretMaterial",
        "OAuthTokenSetSecretMaterial",
    ]
    metadata: Union[Unset, "Metadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.aws_credentials_secret_material import (
            AWSCredentialsSecretMaterial,
        )
        from ..models.generic_secret_material import GenericSecretMaterial
        from ..models.o_auth_token_set_secret_material import (
            OAuthTokenSetSecretMaterial,
        )
        from ..models.org_secret_owner_input import OrgSecretOwnerInput
        from ..models.project_secret_owner_input import ProjectSecretOwnerInput

        owner: dict[str, Any]
        if isinstance(self.owner, OrgSecretOwnerInput):
            owner = self.owner.to_dict()
        elif isinstance(self.owner, ProjectSecretOwnerInput):
            owner = self.owner.to_dict()
        else:
            owner = self.owner.to_dict()

        name = self.name

        material: dict[str, Any]
        if isinstance(self.material, GenericSecretMaterial):
            material = self.material.to_dict()
        elif isinstance(self.material, OAuthTokenSetSecretMaterial):
            material = self.material.to_dict()
        elif isinstance(self.material, AWSCredentialsSecretMaterial):
            material = self.material.to_dict()
        else:
            material = self.material.to_dict()

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "owner": owner,
                "name": name,
                "material": material,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

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
        from ..models.metadata import Metadata
        from ..models.o_auth_token_set_secret_material import (
            OAuthTokenSetSecretMaterial,
        )
        from ..models.org_secret_owner_input import OrgSecretOwnerInput
        from ..models.project_secret_owner_input import ProjectSecretOwnerInput
        from ..models.user_secret_owner_input import UserSecretOwnerInput

        d = dict(src_dict)

        def _parse_owner(
            data: object,
        ) -> Union[
            "OrgSecretOwnerInput", "ProjectSecretOwnerInput", "UserSecretOwnerInput"
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_secret_owner_input_type_0 = (
                    OrgSecretOwnerInput.from_dict(data)
                )

                return componentsschemas_secret_owner_input_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_secret_owner_input_type_1 = (
                    ProjectSecretOwnerInput.from_dict(data)
                )

                return componentsschemas_secret_owner_input_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_secret_owner_input_type_2 = (
                UserSecretOwnerInput.from_dict(data)
            )

            return componentsschemas_secret_owner_input_type_2

        owner = _parse_owner(d.pop("owner"))

        name = d.pop("name")

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

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, Metadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        create_secret_request = cls(
            owner=owner,
            name=name,
            material=material,
            metadata=metadata,
        )

        return create_secret_request
