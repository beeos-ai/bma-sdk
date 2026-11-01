from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.mcp_connection_origin import (
    MCPConnectionOrigin,
    check_mcp_connection_origin,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.compiled_mcp_auth_bearer import CompiledMCPAuthBearer
    from ..models.compiled_mcp_auth_o_auth import CompiledMCPAuthOAuth
    from ..models.compiled_mcp_auth_sig_v4 import CompiledMCPAuthSigV4
    from ..models.compiled_mcp_server_tools import CompiledMCPServerTools
    from ..models.compiled_mcp_transport import CompiledMCPTransport
    from ..models.tool_permission_selection import ToolPermissionSelection


T = TypeVar("T", bound="CompiledMCPServer")


@_attrs_define
class CompiledMCPServer:
    """
    Attributes:
        default_enabled (bool):
        permission (ToolPermissionSelection):
        url (Union[Unset, str]):
        connection_origin (Union[Unset, MCPConnectionOrigin]): Who connects an MCP server. `environment` means the
            executor starts or connects it in its own credential scope; `service` means the harness connects it and keeps
            its credentials.
        transport (Union[Unset, CompiledMCPTransport]): Transport of an environment-origin MCP server.
        auth (Union['CompiledMCPAuthBearer', 'CompiledMCPAuthOAuth', 'CompiledMCPAuthSigV4', Unset]):
        deferred (Union[Unset, bool]):
        tools (Union[Unset, CompiledMCPServerTools]):
    """

    default_enabled: bool
    permission: "ToolPermissionSelection"
    url: Union[Unset, str] = UNSET
    connection_origin: Union[Unset, MCPConnectionOrigin] = UNSET
    transport: Union[Unset, "CompiledMCPTransport"] = UNSET
    auth: Union[
        "CompiledMCPAuthBearer", "CompiledMCPAuthOAuth", "CompiledMCPAuthSigV4", Unset
    ] = UNSET
    deferred: Union[Unset, bool] = UNSET
    tools: Union[Unset, "CompiledMCPServerTools"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.compiled_mcp_auth_bearer import CompiledMCPAuthBearer
        from ..models.compiled_mcp_auth_o_auth import CompiledMCPAuthOAuth

        default_enabled = self.default_enabled

        permission = self.permission.to_dict()

        url = self.url

        connection_origin: Union[Unset, str] = UNSET
        if not isinstance(self.connection_origin, Unset):
            connection_origin = self.connection_origin

        transport: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.transport, Unset):
            transport = self.transport.to_dict()

        auth: Union[Unset, dict[str, Any]]
        if isinstance(self.auth, Unset):
            auth = UNSET
        elif isinstance(self.auth, CompiledMCPAuthBearer):
            auth = self.auth.to_dict()
        elif isinstance(self.auth, CompiledMCPAuthOAuth):
            auth = self.auth.to_dict()
        else:
            auth = self.auth.to_dict()

        deferred = self.deferred

        tools: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tools, Unset):
            tools = self.tools.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "default_enabled": default_enabled,
                "permission": permission,
            }
        )
        if url is not UNSET:
            field_dict["url"] = url
        if connection_origin is not UNSET:
            field_dict["connection_origin"] = connection_origin
        if transport is not UNSET:
            field_dict["transport"] = transport
        if auth is not UNSET:
            field_dict["auth"] = auth
        if deferred is not UNSET:
            field_dict["deferred"] = deferred
        if tools is not UNSET:
            field_dict["tools"] = tools

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.compiled_mcp_auth_bearer import CompiledMCPAuthBearer
        from ..models.compiled_mcp_auth_o_auth import CompiledMCPAuthOAuth
        from ..models.compiled_mcp_auth_sig_v4 import CompiledMCPAuthSigV4
        from ..models.compiled_mcp_server_tools import CompiledMCPServerTools
        from ..models.compiled_mcp_transport import CompiledMCPTransport
        from ..models.tool_permission_selection import ToolPermissionSelection

        d = dict(src_dict)
        default_enabled = d.pop("default_enabled")

        permission = ToolPermissionSelection.from_dict(d.pop("permission"))

        url = d.pop("url", UNSET)

        _connection_origin = d.pop("connection_origin", UNSET)
        connection_origin: Union[Unset, MCPConnectionOrigin]
        if isinstance(_connection_origin, Unset):
            connection_origin = UNSET
        else:
            connection_origin = check_mcp_connection_origin(_connection_origin)

        _transport = d.pop("transport", UNSET)
        transport: Union[Unset, CompiledMCPTransport]
        if isinstance(_transport, Unset):
            transport = UNSET
        else:
            transport = CompiledMCPTransport.from_dict(_transport)

        def _parse_auth(
            data: object,
        ) -> Union[
            "CompiledMCPAuthBearer",
            "CompiledMCPAuthOAuth",
            "CompiledMCPAuthSigV4",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_compiled_mcp_auth_type_0 = (
                    CompiledMCPAuthBearer.from_dict(data)
                )

                return componentsschemas_compiled_mcp_auth_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_compiled_mcp_auth_type_1 = (
                    CompiledMCPAuthOAuth.from_dict(data)
                )

                return componentsschemas_compiled_mcp_auth_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_compiled_mcp_auth_type_2 = CompiledMCPAuthSigV4.from_dict(
                data
            )

            return componentsschemas_compiled_mcp_auth_type_2

        auth = _parse_auth(d.pop("auth", UNSET))

        deferred = d.pop("deferred", UNSET)

        _tools = d.pop("tools", UNSET)
        tools: Union[Unset, CompiledMCPServerTools]
        if isinstance(_tools, Unset):
            tools = UNSET
        else:
            tools = CompiledMCPServerTools.from_dict(_tools)

        compiled_mcp_server = cls(
            default_enabled=default_enabled,
            permission=permission,
            url=url,
            connection_origin=connection_origin,
            transport=transport,
            auth=auth,
            deferred=deferred,
            tools=tools,
        )

        return compiled_mcp_server
