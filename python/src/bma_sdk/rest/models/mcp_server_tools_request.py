from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.mcp_server_auth_bearer import MCPServerAuthBearer
    from ..models.mcp_server_auth_none import MCPServerAuthNone
    from ..models.mcp_server_auth_o_auth import MCPServerAuthOAuth
    from ..models.mcp_server_auth_sig_v4 import MCPServerAuthSigV4


T = TypeVar("T", bound="MCPServerToolsRequest")


@_attrs_define
class MCPServerToolsRequest:
    """
    Attributes:
        url (str): Streamable HTTP MCP endpoint. Must use HTTPS, except that HTTP is allowed for loopback hosts during
            local development.
        auth (Union['MCPServerAuthBearer', 'MCPServerAuthNone', 'MCPServerAuthOAuth', 'MCPServerAuthSigV4']): How BMA
            authenticates to the MCP server. Secret references must be available to the project, either owned by it or
            granted to it.
    """

    url: str
    auth: Union[
        "MCPServerAuthBearer",
        "MCPServerAuthNone",
        "MCPServerAuthOAuth",
        "MCPServerAuthSigV4",
    ]

    def to_dict(self) -> dict[str, Any]:
        from ..models.mcp_server_auth_bearer import MCPServerAuthBearer
        from ..models.mcp_server_auth_none import MCPServerAuthNone
        from ..models.mcp_server_auth_o_auth import MCPServerAuthOAuth

        url = self.url

        auth: dict[str, Any]
        if isinstance(self.auth, MCPServerAuthNone):
            auth = self.auth.to_dict()
        elif isinstance(self.auth, MCPServerAuthBearer):
            auth = self.auth.to_dict()
        elif isinstance(self.auth, MCPServerAuthOAuth):
            auth = self.auth.to_dict()
        else:
            auth = self.auth.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "url": url,
                "auth": auth,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mcp_server_auth_bearer import MCPServerAuthBearer
        from ..models.mcp_server_auth_none import MCPServerAuthNone
        from ..models.mcp_server_auth_o_auth import MCPServerAuthOAuth
        from ..models.mcp_server_auth_sig_v4 import MCPServerAuthSigV4

        d = dict(src_dict)
        url = d.pop("url")

        def _parse_auth(
            data: object,
        ) -> Union[
            "MCPServerAuthBearer",
            "MCPServerAuthNone",
            "MCPServerAuthOAuth",
            "MCPServerAuthSigV4",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_mcp_server_auth_type_0 = MCPServerAuthNone.from_dict(
                    data
                )

                return componentsschemas_mcp_server_auth_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_mcp_server_auth_type_1 = (
                    MCPServerAuthBearer.from_dict(data)
                )

                return componentsschemas_mcp_server_auth_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_mcp_server_auth_type_2 = MCPServerAuthOAuth.from_dict(
                    data
                )

                return componentsschemas_mcp_server_auth_type_2
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_mcp_server_auth_type_3 = MCPServerAuthSigV4.from_dict(
                data
            )

            return componentsschemas_mcp_server_auth_type_3

        auth = _parse_auth(d.pop("auth"))

        mcp_server_tools_request = cls(
            url=url,
            auth=auth,
        )

        return mcp_server_tools_request
