from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.o_auth_token_set_secret_material_kind import (
    OAuthTokenSetSecretMaterialKind,
    check_o_auth_token_set_secret_material_kind,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.o_auth_refresh_secret_material import OAuthRefreshSecretMaterial


T = TypeVar("T", bound="OAuthTokenSetSecretMaterial")


@_attrs_define
class OAuthTokenSetSecretMaterial:
    """
    Attributes:
        kind (OAuthTokenSetSecretMaterialKind):
        access_token (str):
        access_token_expires_in_seconds (Union[Unset, int]):
        refresh (Union[Unset, OAuthRefreshSecretMaterial]):
        id_token (Union[Unset, str]):
        mcp_url (Union[Unset, str]):
        scopes (Union[Unset, str]):
        token_type (Union[Unset, str]):
    """

    kind: OAuthTokenSetSecretMaterialKind
    access_token: str
    access_token_expires_in_seconds: Union[Unset, int] = UNSET
    refresh: Union[Unset, "OAuthRefreshSecretMaterial"] = UNSET
    id_token: Union[Unset, str] = UNSET
    mcp_url: Union[Unset, str] = UNSET
    scopes: Union[Unset, str] = UNSET
    token_type: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        access_token = self.access_token

        access_token_expires_in_seconds = self.access_token_expires_in_seconds

        refresh: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.refresh, Unset):
            refresh = self.refresh.to_dict()

        id_token = self.id_token

        mcp_url = self.mcp_url

        scopes = self.scopes

        token_type = self.token_type

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "access_token": access_token,
            }
        )
        if access_token_expires_in_seconds is not UNSET:
            field_dict["access_token_expires_in_seconds"] = (
                access_token_expires_in_seconds
            )
        if refresh is not UNSET:
            field_dict["refresh"] = refresh
        if id_token is not UNSET:
            field_dict["id_token"] = id_token
        if mcp_url is not UNSET:
            field_dict["mcp_url"] = mcp_url
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if token_type is not UNSET:
            field_dict["token_type"] = token_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.o_auth_refresh_secret_material import OAuthRefreshSecretMaterial

        d = dict(src_dict)
        kind = check_o_auth_token_set_secret_material_kind(d.pop("kind"))

        access_token = d.pop("access_token")

        access_token_expires_in_seconds = d.pop(
            "access_token_expires_in_seconds", UNSET
        )

        _refresh = d.pop("refresh", UNSET)
        refresh: Union[Unset, OAuthRefreshSecretMaterial]
        if isinstance(_refresh, Unset):
            refresh = UNSET
        else:
            refresh = OAuthRefreshSecretMaterial.from_dict(_refresh)

        id_token = d.pop("id_token", UNSET)

        mcp_url = d.pop("mcp_url", UNSET)

        scopes = d.pop("scopes", UNSET)

        token_type = d.pop("token_type", UNSET)

        o_auth_token_set_secret_material = cls(
            kind=kind,
            access_token=access_token,
            access_token_expires_in_seconds=access_token_expires_in_seconds,
            refresh=refresh,
            id_token=id_token,
            mcp_url=mcp_url,
            scopes=scopes,
            token_type=token_type,
        )

        return o_auth_token_set_secret_material
