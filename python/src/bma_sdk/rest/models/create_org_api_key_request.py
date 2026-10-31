from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.org_api_key_role import OrgAPIKeyRole, check_org_api_key_role

T = TypeVar("T", bound="CreateOrgAPIKeyRequest")


@_attrs_define
class CreateOrgAPIKeyRequest:
    """
    Attributes:
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        org_role (OrgAPIKeyRole): The key's org role. Org API keys can never hold the owner role.
    """

    name: str
    org_role: OrgAPIKeyRole

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        org_role: str = self.org_role

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "org_role": org_role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        org_role = check_org_api_key_role(d.pop("org_role"))

        create_org_api_key_request = cls(
            name=name,
            org_role=org_role,
        )

        return create_org_api_key_request
