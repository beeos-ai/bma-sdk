from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.agent_input import AgentInput


T = TypeVar("T", bound="AgentInputEnvelope")


@_attrs_define
class AgentInputEnvelope:
    """
    Attributes:
        agent_input (AgentInput):
    """

    agent_input: "AgentInput"

    def to_dict(self) -> dict[str, Any]:
        agent_input = self.agent_input.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "agent_input": agent_input,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_input import AgentInput

        d = dict(src_dict)
        agent_input = AgentInput.from_dict(d.pop("agent_input"))

        agent_input_envelope = cls(
            agent_input=agent_input,
        )

        return agent_input_envelope
