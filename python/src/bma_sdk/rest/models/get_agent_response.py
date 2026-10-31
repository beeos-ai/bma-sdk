from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.agent import Agent
    from ..models.agent_mcp_connection import AgentMCPConnection


T = TypeVar("T", bound="GetAgentResponse")


@_attrs_define
class GetAgentResponse:
    """
    Attributes:
        agent (Agent):
        machine_ids (list[str]): Machines currently attached to the agent, in binding creation order.
        mcp_connections (list['AgentMCPConnection']): The agent's MCP server connections, ordered by server key.
    """

    agent: "Agent"
    machine_ids: list[str]
    mcp_connections: list["AgentMCPConnection"]

    def to_dict(self) -> dict[str, Any]:
        agent = self.agent.to_dict()

        machine_ids = self.machine_ids

        mcp_connections = []
        for mcp_connections_item_data in self.mcp_connections:
            mcp_connections_item = mcp_connections_item_data.to_dict()
            mcp_connections.append(mcp_connections_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "agent": agent,
                "machine_ids": machine_ids,
                "mcp_connections": mcp_connections,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent import Agent
        from ..models.agent_mcp_connection import AgentMCPConnection

        d = dict(src_dict)
        agent = Agent.from_dict(d.pop("agent"))

        machine_ids = cast(list[str], d.pop("machine_ids"))

        mcp_connections = []
        _mcp_connections = d.pop("mcp_connections")
        for mcp_connections_item_data in _mcp_connections:
            mcp_connections_item = AgentMCPConnection.from_dict(
                mcp_connections_item_data
            )

            mcp_connections.append(mcp_connections_item)

        get_agent_response = cls(
            agent=agent,
            machine_ids=machine_ids,
            mcp_connections=mcp_connections,
        )

        return get_agent_response
