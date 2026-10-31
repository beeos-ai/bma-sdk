from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.org_api_key_role import OrgAPIKeyRole, check_org_api_key_role
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateOrgAPIKeyRequest")


@_attrs_define
class UpdateOrgAPIKeyRequest:
    """
    Attributes:
        name (Union[Unset, str]): Human-readable name. Spaces and punctuation are allowed; leading or trailing
            whitespace and invisible or control characters are not.
        org_role (Union[Unset, OrgAPIKeyRole]): The key's org role. Org API keys can never hold the owner role.
    """

    name: Union[Unset, str] = UNSET
    org_role: Union[Unset, OrgAPIKeyRole] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        org_role: Union[Unset, str] = UNSET
        if not isinstance(self.org_role, Unset):
            org_role = self.org_role

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if org_role is not UNSET:
            field_dict["org_role"] = org_role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _org_role = d.pop("org_role", UNSET)
        org_role: Union[Unset, OrgAPIKeyRole]
        if isinstance(_org_role, Unset):
            org_role = UNSET
        else:
            org_role = check_org_api_key_role(_org_role)

        update_org_api_key_request = cls(
            name=name,
            org_role=org_role,
        )

        return update_org_api_key_request
