from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mcpo_auth_start_metadata import MCPOAuthStartMetadata
    from ..models.org_secret_owner_input import OrgSecretOwnerInput
    from ..models.project_secret_owner_input import ProjectSecretOwnerInput
    from ..models.user_secret_owner_input import UserSecretOwnerInput


T = TypeVar("T", bound="MCPOAuthStartRequest")


@_attrs_define
class MCPOAuthStartRequest:
    """
    Attributes:
        owner (Union['OrgSecretOwnerInput', 'ProjectSecretOwnerInput', 'UserSecretOwnerInput']): Who owns the secret:
            {"kind":"org"}, {"kind":"project","project_id":"proj_..."}, or {"kind":"user"}. The owner cannot change later.
        mcp_url (str):
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        return_to (Union[Unset, str]):
        client_id (Union[Unset, str]):
        client_secret (Union[Unset, str]):
        scopes (Union[Unset, list[str]]):
        metadata (Union[Unset, MCPOAuthStartMetadata]): User-supplied metadata for the stored secret. A restriction of
            Metadata that leaves room for one reserved pair - BMA sets mcp_url on the secret to the flow's MCP endpoint URL,
            so the key is reserved and at most 15 user pairs are accepted.
    """

    owner: Union[
        "OrgSecretOwnerInput", "ProjectSecretOwnerInput", "UserSecretOwnerInput"
    ]
    mcp_url: str
    name: str
    return_to: Union[Unset, str] = UNSET
    client_id: Union[Unset, str] = UNSET
    client_secret: Union[Unset, str] = UNSET
    scopes: Union[Unset, list[str]] = UNSET
    metadata: Union[Unset, "MCPOAuthStartMetadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.org_secret_owner_input import OrgSecretOwnerInput
        from ..models.project_secret_owner_input import ProjectSecretOwnerInput

        owner: dict[str, Any]
        if isinstance(self.owner, OrgSecretOwnerInput):
            owner = self.owner.to_dict()
        elif isinstance(self.owner, ProjectSecretOwnerInput):
            owner = self.owner.to_dict()
        else:
            owner = self.owner.to_dict()

        mcp_url = self.mcp_url

        name = self.name

        return_to = self.return_to

        client_id = self.client_id

        client_secret = self.client_secret

        scopes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "owner": owner,
                "mcp_url": mcp_url,
                "name": name,
            }
        )
        if return_to is not UNSET:
            field_dict["return_to"] = return_to
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_secret is not UNSET:
            field_dict["client_secret"] = client_secret
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mcpo_auth_start_metadata import MCPOAuthStartMetadata
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

        mcp_url = d.pop("mcp_url")

        name = d.pop("name")

        return_to = d.pop("return_to", UNSET)

        client_id = d.pop("client_id", UNSET)

        client_secret = d.pop("client_secret", UNSET)

        scopes = cast(list[str], d.pop("scopes", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, MCPOAuthStartMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = MCPOAuthStartMetadata.from_dict(_metadata)

        mcpo_auth_start_request = cls(
            owner=owner,
            mcp_url=mcp_url,
            name=name,
            return_to=return_to,
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes,
            metadata=metadata,
        )

        return mcpo_auth_start_request
