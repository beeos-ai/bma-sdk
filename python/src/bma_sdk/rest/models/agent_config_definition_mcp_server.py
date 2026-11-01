from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..models.mcp_connection_origin import (
    MCPConnectionOrigin,
    check_mcp_connection_origin,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config_definition_mcp_auth import AgentConfigDefinitionMCPAuth
    from ..models.agent_config_definition_mcp_server_tools import (
        AgentConfigDefinitionMCPServerTools,
    )
    from ..models.agent_config_definition_mcp_transport import (
        AgentConfigDefinitionMCPTransport,
    )
    from ..models.agent_config_definition_tool_permission import (
        AgentConfigDefinitionToolPermission,
    )


T = TypeVar("T", bound="AgentConfigDefinitionMCPServer")


@_attrs_define
class AgentConfigDefinitionMCPServer:
    """
    Attributes:
        auth (Union[Unset, AgentConfigDefinitionMCPAuth]):
        connection_origin (Union[Unset, MCPConnectionOrigin]): Who connects an MCP server. `environment` means the
            executor starts or connects it in its own credential scope; `service` means the harness connects it and keeps
            its credentials.
        default_enabled (Union[None, Unset, bool]):
        deferred (Union[Unset, bool]):
        permission (Union[Unset, AgentConfigDefinitionToolPermission]):
        tools (Union[Unset, AgentConfigDefinitionMCPServerTools]):
        transport (Union[Unset, AgentConfigDefinitionMCPTransport]): Transport of an environment-origin MCP server.
            stdio requires `command`; http requires `url`. No shell is involved: `command` is one executable token. `env`
            values that name a secret stay references; the executor resolves them in its own credential scope.
        url (Union[Unset, str]):
    """

    auth: Union[Unset, "AgentConfigDefinitionMCPAuth"] = UNSET
    connection_origin: Union[Unset, MCPConnectionOrigin] = UNSET
    default_enabled: Union[None, Unset, bool] = UNSET
    deferred: Union[Unset, bool] = UNSET
    permission: Union[Unset, "AgentConfigDefinitionToolPermission"] = UNSET
    tools: Union[Unset, "AgentConfigDefinitionMCPServerTools"] = UNSET
    transport: Union[Unset, "AgentConfigDefinitionMCPTransport"] = UNSET
    url: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        auth: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.auth, Unset):
            auth = self.auth.to_dict()

        connection_origin: Union[Unset, str] = UNSET
        if not isinstance(self.connection_origin, Unset):
            connection_origin = self.connection_origin

        default_enabled: Union[None, Unset, bool]
        if isinstance(self.default_enabled, Unset):
            default_enabled = UNSET
        else:
            default_enabled = self.default_enabled

        deferred = self.deferred

        permission: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.permission, Unset):
            permission = self.permission.to_dict()

        tools: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.tools, Unset):
            tools = self.tools.to_dict()

        transport: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.transport, Unset):
            transport = self.transport.to_dict()

        url = self.url

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if auth is not UNSET:
            field_dict["auth"] = auth
        if connection_origin is not UNSET:
            field_dict["connection_origin"] = connection_origin
        if default_enabled is not UNSET:
            field_dict["default_enabled"] = default_enabled
        if deferred is not UNSET:
            field_dict["deferred"] = deferred
        if permission is not UNSET:
            field_dict["permission"] = permission
        if tools is not UNSET:
            field_dict["tools"] = tools
        if transport is not UNSET:
            field_dict["transport"] = transport
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_definition_mcp_auth import (
            AgentConfigDefinitionMCPAuth,
        )
        from ..models.agent_config_definition_mcp_server_tools import (
            AgentConfigDefinitionMCPServerTools,
        )
        from ..models.agent_config_definition_mcp_transport import (
            AgentConfigDefinitionMCPTransport,
        )
        from ..models.agent_config_definition_tool_permission import (
            AgentConfigDefinitionToolPermission,
        )

        d = dict(src_dict)
        _auth = d.pop("auth", UNSET)
        auth: Union[Unset, AgentConfigDefinitionMCPAuth]
        if isinstance(_auth, Unset):
            auth = UNSET
        else:
            auth = AgentConfigDefinitionMCPAuth.from_dict(_auth)

        _connection_origin = d.pop("connection_origin", UNSET)
        connection_origin: Union[Unset, MCPConnectionOrigin]
        if isinstance(_connection_origin, Unset):
            connection_origin = UNSET
        else:
            connection_origin = check_mcp_connection_origin(_connection_origin)

        def _parse_default_enabled(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        default_enabled = _parse_default_enabled(d.pop("default_enabled", UNSET))

        deferred = d.pop("deferred", UNSET)

        _permission = d.pop("permission", UNSET)
        permission: Union[Unset, AgentConfigDefinitionToolPermission]
        if isinstance(_permission, Unset):
            permission = UNSET
        else:
            permission = AgentConfigDefinitionToolPermission.from_dict(_permission)

        _tools = d.pop("tools", UNSET)
        tools: Union[Unset, AgentConfigDefinitionMCPServerTools]
        if isinstance(_tools, Unset):
            tools = UNSET
        else:
            tools = AgentConfigDefinitionMCPServerTools.from_dict(_tools)

        _transport = d.pop("transport", UNSET)
        transport: Union[Unset, AgentConfigDefinitionMCPTransport]
        if isinstance(_transport, Unset):
            transport = UNSET
        else:
            transport = AgentConfigDefinitionMCPTransport.from_dict(_transport)

        url = d.pop("url", UNSET)

        agent_config_definition_mcp_server = cls(
            auth=auth,
            connection_origin=connection_origin,
            default_enabled=default_enabled,
            deferred=deferred,
            permission=permission,
            tools=tools,
            transport=transport,
            url=url,
        )

        return agent_config_definition_mcp_server
