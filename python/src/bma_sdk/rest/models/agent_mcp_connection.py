import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.agent_mcp_connection_state import (
    AgentMCPConnectionState,
    check_agent_mcp_connection_state,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentMCPConnection")


@_attrs_define
class AgentMCPConnection:
    """
    Attributes:
        server_key (str):
        endpoint_url (str):
        state (AgentMCPConnectionState):
        initialize_error (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        protocol_version (Union[Unset, str]):
    """

    server_key: str
    endpoint_url: str
    state: AgentMCPConnectionState
    initialize_error: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    protocol_version: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        server_key = self.server_key

        endpoint_url = self.endpoint_url

        state: str = self.state

        initialize_error = self.initialize_error

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        protocol_version = self.protocol_version

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "server_key": server_key,
                "endpoint_url": endpoint_url,
                "state": state,
                "initialize_error": initialize_error,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if protocol_version is not UNSET:
            field_dict["protocol_version"] = protocol_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        server_key = d.pop("server_key")

        endpoint_url = d.pop("endpoint_url")

        state = check_agent_mcp_connection_state(d.pop("state"))

        initialize_error = d.pop("initialize_error")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        protocol_version = d.pop("protocol_version", UNSET)

        agent_mcp_connection = cls(
            server_key=server_key,
            endpoint_url=endpoint_url,
            state=state,
            initialize_error=initialize_error,
            created_at=created_at,
            updated_at=updated_at,
            protocol_version=protocol_version,
        )

        return agent_mcp_connection
