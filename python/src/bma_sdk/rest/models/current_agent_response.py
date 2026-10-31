from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.agent import Agent


T = TypeVar("T", bound="CurrentAgentResponse")


@_attrs_define
class CurrentAgentResponse:
    """
    Attributes:
        agent (Agent):
    """

    agent: "Agent"

    def to_dict(self) -> dict[str, Any]:
        agent = self.agent.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "agent": agent,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent import Agent

        d = dict(src_dict)
        agent = Agent.from_dict(d.pop("agent"))

        current_agent_response = cls(
            agent=agent,
        )

        return current_agent_response
