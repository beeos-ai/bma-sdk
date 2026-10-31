from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.compiled_mcp_auth_bearer import CompiledMCPAuthBearer
    from ..models.compiled_mcp_auth_o_auth import CompiledMCPAuthOAuth
    from ..models.compiled_mcp_auth_sig_v4 import CompiledMCPAuthSigV4
    from ..models.compiled_mcp_server_tools import CompiledMCPServerTools
    from ..models.tool_permission_selection import ToolPermissionSelection


T = TypeVar("T", bound="CompiledMCPServer")


@_attrs_define
class CompiledMCPServer:
    """
    Attributes:
        url (str):
        default_enabled (bool):
        permission (ToolPermissionSelection):
        auth (Union['CompiledMCPAuthBearer', 'CompiledMCPAuthOAuth', 'CompiledMCPAuthSigV4', Unset]):
        deferred (Union[Unset, bool]):
        tools (Union[Unset, CompiledMCPServerTools]):
    """

    url: str
    default_enabled: bool
    permission: "ToolPermissionSelection"
    auth: Union[
        "CompiledMCPAuthBearer", "CompiledMCPAuthOAuth", "CompiledMCPAuthSigV4", Unset
    ] = UNSET
    deferred: Union[Unset, bool] = UNSET
    tools: Union[Unset, "CompiledMCPServerTools"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.compiled_mcp_auth_bearer import CompiledMCPAuthBearer
        from ..models.compiled_mcp_auth_o_auth import CompiledMCPAuthOAuth

        url = self.url

        default_enabled = self.default_enabled

        permission = self.permission.to_dict()

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
                "url": url,
                "default_enabled": default_enabled,
                "permission": permission,
            }
        )
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
        from ..models.tool_permission_selection import ToolPermissionSelection

        d = dict(src_dict)
        url = d.pop("url")

        default_enabled = d.pop("default_enabled")

        permission = ToolPermissionSelection.from_dict(d.pop("permission"))

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
            url=url,
            default_enabled=default_enabled,
            permission=permission,
            auth=auth,
            deferred=deferred,
            tools=tools,
        )

        return compiled_mcp_server
