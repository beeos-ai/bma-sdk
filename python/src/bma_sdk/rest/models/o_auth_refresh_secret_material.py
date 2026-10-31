from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="OAuthRefreshSecretMaterial")


@_attrs_define
class OAuthRefreshSecretMaterial:
    """
    Attributes:
        refresh_token (str):
        token_endpoint (str): Must use HTTPS, except that HTTP is allowed for loopback hosts during local development.
        client_id (str):
        resource (str):
        client_secret (Union[Unset, str]):
    """

    refresh_token: str
    token_endpoint: str
    client_id: str
    resource: str
    client_secret: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        refresh_token = self.refresh_token

        token_endpoint = self.token_endpoint

        client_id = self.client_id

        resource = self.resource

        client_secret = self.client_secret

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "refresh_token": refresh_token,
                "token_endpoint": token_endpoint,
                "client_id": client_id,
                "resource": resource,
            }
        )
        if client_secret is not UNSET:
            field_dict["client_secret"] = client_secret

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        refresh_token = d.pop("refresh_token")

        token_endpoint = d.pop("token_endpoint")

        client_id = d.pop("client_id")

        resource = d.pop("resource")

        client_secret = d.pop("client_secret", UNSET)

        o_auth_refresh_secret_material = cls(
            refresh_token=refresh_token,
            token_endpoint=token_endpoint,
            client_id=client_id,
            resource=resource,
            client_secret=client_secret,
        )

        return o_auth_refresh_secret_material
