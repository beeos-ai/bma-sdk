from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.agent_config_definition_harness_kind import (
    AgentConfigDefinitionHarnessKind,
    check_agent_config_definition_harness_kind,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentConfigDefinitionHarness")


@_attrs_define
class AgentConfigDefinitionHarness:
    """Experimental. Which brain runs the agent's sessions: what it is, not where it runs. Omitted, or kind bma, is the BMA
    harness, which always runs on the server. Kind acp runs an Agent Client Protocol agent (agent dsh) on the session's
    machine and requires machine_sources; where it runs follows the session's machine sources (a machine pool is a
    sandbox, a BYO machine is local).

        Attributes:
            kind (AgentConfigDefinitionHarnessKind):
            agent (Union[Unset, str]):
    """

    kind: AgentConfigDefinitionHarnessKind
    agent: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        agent = self.agent

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
            }
        )
        if agent is not UNSET:
            field_dict["agent"] = agent

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_agent_config_definition_harness_kind(d.pop("kind"))

        agent = d.pop("agent", UNSET)

        agent_config_definition_harness = cls(
            kind=kind,
            agent=agent,
        )

        return agent_config_definition_harness
