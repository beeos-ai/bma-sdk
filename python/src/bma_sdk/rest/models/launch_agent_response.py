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
    from ..models.agent import Agent
    from ..models.agent_config import AgentConfig
    from ..models.agent_input import AgentInput
    from ..models.agent_machine_binding import AgentMachineBinding


T = TypeVar("T", bound="LaunchAgentResponse")


@_attrs_define
class LaunchAgentResponse:
    """
    Attributes:
        agent (Agent):
        agent_config (AgentConfig):
        machine_bindings (list['AgentMachineBinding']):
        agent_input (Union[Unset, AgentInput]):
    """

    agent: "Agent"
    agent_config: "AgentConfig"
    machine_bindings: list["AgentMachineBinding"]
    agent_input: Union[Unset, "AgentInput"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        agent = self.agent.to_dict()

        agent_config = self.agent_config.to_dict()

        machine_bindings = []
        for machine_bindings_item_data in self.machine_bindings:
            machine_bindings_item = machine_bindings_item_data.to_dict()
            machine_bindings.append(machine_bindings_item)

        agent_input: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.agent_input, Unset):
            agent_input = self.agent_input.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "agent": agent,
                "agent_config": agent_config,
                "machine_bindings": machine_bindings,
            }
        )
        if agent_input is not UNSET:
            field_dict["agent_input"] = agent_input

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent import Agent
        from ..models.agent_config import AgentConfig
        from ..models.agent_input import AgentInput
        from ..models.agent_machine_binding import AgentMachineBinding

        d = dict(src_dict)
        agent = Agent.from_dict(d.pop("agent"))

        agent_config = AgentConfig.from_dict(d.pop("agent_config"))

        machine_bindings = []
        _machine_bindings = d.pop("machine_bindings")
        for machine_bindings_item_data in _machine_bindings:
            machine_bindings_item = AgentMachineBinding.from_dict(
                machine_bindings_item_data
            )

            machine_bindings.append(machine_bindings_item)

        _agent_input = d.pop("agent_input", UNSET)
        agent_input: Union[Unset, AgentInput]
        if isinstance(_agent_input, Unset):
            agent_input = UNSET
        else:
            agent_input = AgentInput.from_dict(_agent_input)

        launch_agent_response = cls(
            agent=agent,
            agent_config=agent_config,
            machine_bindings=machine_bindings,
            agent_input=agent_input,
        )

        return launch_agent_response
