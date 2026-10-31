from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.org_api_key import OrgAPIKey


T = TypeVar("T", bound="CreateOrgAPIKeyResponse")


@_attrs_define
class CreateOrgAPIKeyResponse:
    """
    Attributes:
        token (str): Opaque bearer credential.
        api_key (OrgAPIKey):
    """

    token: str
    api_key: "OrgAPIKey"

    def to_dict(self) -> dict[str, Any]:
        token = self.token

        api_key = self.api_key.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "token": token,
                "api_key": api_key,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.org_api_key import OrgAPIKey

        d = dict(src_dict)
        token = d.pop("token")

        api_key = OrgAPIKey.from_dict(d.pop("api_key"))

        create_org_api_key_response = cls(
            token=token,
            api_key=api_key,
        )

        return create_org_api_key_response
