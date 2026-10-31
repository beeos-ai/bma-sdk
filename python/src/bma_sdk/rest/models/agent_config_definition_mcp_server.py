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
    from ..models.agent_config_definition_mcp_auth import AgentConfigDefinitionMCPAuth
    from ..models.agent_config_definition_mcp_server_tools import (
        AgentConfigDefinitionMCPServerTools,
    )
    from ..models.agent_config_definition_tool_permission import (
        AgentConfigDefinitionToolPermission,
    )


T = TypeVar("T", bound="AgentConfigDefinitionMCPServer")


@_attrs_define
class AgentConfigDefinitionMCPServer:
    """
    Attributes:
        url (str):
        auth (Union[Unset, AgentConfigDefinitionMCPAuth]):
        default_enabled (Union[None, Unset, bool]):
        deferred (Union[Unset, bool]):
        permission (Union[Unset, AgentConfigDefinitionToolPermission]):
        tools (Union[Unset, AgentConfigDefinitionMCPServerTools]):
    """

    url: str
    auth: Union[Unset, "AgentConfigDefinitionMCPAuth"] = UNSET
    default_enabled: Union[None, Unset, bool] = UNSET
    deferred: Union[Unset, bool] = UNSET
    permission: Union[Unset, "AgentConfigDefinitionToolPermission"] = UNSET
    tools: Union[Unset, "AgentConfigDefinitionMCPServerTools"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        auth: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.auth, Unset):
            auth = self.auth.to_dict()

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

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "url": url,
            }
        )
        if auth is not UNSET:
            field_dict["auth"] = auth
        if default_enabled is not UNSET:
            field_dict["default_enabled"] = default_enabled
        if deferred is not UNSET:
            field_dict["deferred"] = deferred
        if permission is not UNSET:
            field_dict["permission"] = permission
        if tools is not UNSET:
            field_dict["tools"] = tools

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_definition_mcp_auth import (
            AgentConfigDefinitionMCPAuth,
        )
        from ..models.agent_config_definition_mcp_server_tools import (
            AgentConfigDefinitionMCPServerTools,
        )
        from ..models.agent_config_definition_tool_permission import (
            AgentConfigDefinitionToolPermission,
        )

        d = dict(src_dict)
        url = d.pop("url")

        _auth = d.pop("auth", UNSET)
        auth: Union[Unset, AgentConfigDefinitionMCPAuth]
        if isinstance(_auth, Unset):
            auth = UNSET
        else:
            auth = AgentConfigDefinitionMCPAuth.from_dict(_auth)

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

        agent_config_definition_mcp_server = cls(
            url=url,
            auth=auth,
            default_enabled=default_enabled,
            deferred=deferred,
            permission=permission,
            tools=tools,
        )

        return agent_config_definition_mcp_server
