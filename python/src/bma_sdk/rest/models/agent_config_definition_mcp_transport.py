from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..models.mcp_transport_type import MCPTransportType, check_mcp_transport_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config_definition_mcp_transport_env import (
        AgentConfigDefinitionMCPTransportEnv,
    )


T = TypeVar("T", bound="AgentConfigDefinitionMCPTransport")


@_attrs_define
class AgentConfigDefinitionMCPTransport:
    """Transport of an environment-origin MCP server. stdio requires `command`; http requires `url`. No shell is involved:
    `command` is one executable token. `env` values that name a secret stay references; the executor resolves them in
    its own credential scope.

        Attributes:
            type_ (MCPTransportType): Transport of an MCP server.
            command (Union[Unset, str]):
            args (Union[Unset, list[str]]):
            cwd (Union[Unset, str]):
            env (Union[Unset, AgentConfigDefinitionMCPTransportEnv]):
            timeout_ms (Union[Unset, int]):
            command_sha256 (Union[Unset, str]):
            url (Union[Unset, str]):
    """

    type_: MCPTransportType
    command: Union[Unset, str] = UNSET
    args: Union[Unset, list[str]] = UNSET
    cwd: Union[Unset, str] = UNSET
    env: Union[Unset, "AgentConfigDefinitionMCPTransportEnv"] = UNSET
    timeout_ms: Union[Unset, int] = UNSET
    command_sha256: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        command = self.command

        args: Union[Unset, list[str]] = UNSET
        if not isinstance(self.args, Unset):
            args = self.args

        cwd = self.cwd

        env: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.env, Unset):
            env = self.env.to_dict()

        timeout_ms = self.timeout_ms

        command_sha256 = self.command_sha256

        url = self.url

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
            }
        )
        if command is not UNSET:
            field_dict["command"] = command
        if args is not UNSET:
            field_dict["args"] = args
        if cwd is not UNSET:
            field_dict["cwd"] = cwd
        if env is not UNSET:
            field_dict["env"] = env
        if timeout_ms is not UNSET:
            field_dict["timeout_ms"] = timeout_ms
        if command_sha256 is not UNSET:
            field_dict["command_sha256"] = command_sha256
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_definition_mcp_transport_env import (
            AgentConfigDefinitionMCPTransportEnv,
        )

        d = dict(src_dict)
        type_ = check_mcp_transport_type(d.pop("type"))

        command = d.pop("command", UNSET)

        args = cast(list[str], d.pop("args", UNSET))

        cwd = d.pop("cwd", UNSET)

        _env = d.pop("env", UNSET)
        env: Union[Unset, AgentConfigDefinitionMCPTransportEnv]
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = AgentConfigDefinitionMCPTransportEnv.from_dict(_env)

        timeout_ms = d.pop("timeout_ms", UNSET)

        command_sha256 = d.pop("command_sha256", UNSET)

        url = d.pop("url", UNSET)

        agent_config_definition_mcp_transport = cls(
            type_=type_,
            command=command,
            args=args,
            cwd=cwd,
            env=env,
            timeout_ms=timeout_ms,
            command_sha256=command_sha256,
            url=url,
        )

        return agent_config_definition_mcp_transport
