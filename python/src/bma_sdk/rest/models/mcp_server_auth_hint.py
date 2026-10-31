from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..models.mcp_server_auth_hint_type import (
    MCPServerAuthHintType,
    check_mcp_server_auth_hint_type,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="MCPServerAuthHint")


@_attrs_define
class MCPServerAuthHint:
    """
    Attributes:
        type_ (MCPServerAuthHintType): `oauth` when the server advertises an OAuth authorization server per the MCP
            authorization spec; `bearer` when it rejects unauthenticated requests without OAuth metadata, which usually
            means a static API token.
        scopes (Union[Unset, list[str]]): Scopes the server requested or supports, when advertised.
        authorization_server (Union[Unset, str]): Issuer URL of the OAuth authorization server, when advertised.
    """

    type_: MCPServerAuthHintType
    scopes: Union[Unset, list[str]] = UNSET
    authorization_server: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        scopes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        authorization_server = self.authorization_server

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
            }
        )
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if authorization_server is not UNSET:
            field_dict["authorization_server"] = authorization_server

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_mcp_server_auth_hint_type(d.pop("type"))

        scopes = cast(list[str], d.pop("scopes", UNSET))

        authorization_server = d.pop("authorization_server", UNSET)

        mcp_server_auth_hint = cls(
            type_=type_,
            scopes=scopes,
            authorization_server=authorization_server,
        )

        return mcp_server_auth_hint
