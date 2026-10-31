from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.agent_config import AgentConfig
    from ..models.agent_input import AgentInput


T = TypeVar("T", bound="UpdateAgentConfigResponse")


@_attrs_define
class UpdateAgentConfigResponse:
    """
    Attributes:
        agent_config (AgentConfig):
        agent_input (AgentInput):
        event_id (str):
    """

    agent_config: "AgentConfig"
    agent_input: "AgentInput"
    event_id: str

    def to_dict(self) -> dict[str, Any]:
        agent_config = self.agent_config.to_dict()

        agent_input = self.agent_input.to_dict()

        event_id = self.event_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "agent_config": agent_config,
                "agent_input": agent_input,
                "event_id": event_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config import AgentConfig
        from ..models.agent_input import AgentInput

        d = dict(src_dict)
        agent_config = AgentConfig.from_dict(d.pop("agent_config"))

        agent_input = AgentInput.from_dict(d.pop("agent_input"))

        event_id = d.pop("event_id")

        update_agent_config_response = cls(
            agent_config=agent_config,
            agent_input=agent_input,
            event_id=event_id,
        )

        return update_agent_config_response
