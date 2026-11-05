from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.agent_interaction_kind import (
    AgentInteractionKind,
    check_agent_interaction_kind,
)
from ..models.agent_interaction_state import (
    AgentInteractionState,
    check_agent_interaction_state,
)

T = TypeVar("T", bound="ExecutorInteractionUpdateInteractionUpdate")


@_attrs_define
class ExecutorInteractionUpdateInteractionUpdate:
    """
    Attributes:
        interaction_id (str):
        state (AgentInteractionState):
        interaction_kind (AgentInteractionKind):
    """

    interaction_id: str
    state: AgentInteractionState
    interaction_kind: AgentInteractionKind

    def to_dict(self) -> dict[str, Any]:
        interaction_id = self.interaction_id

        state: str = self.state

        interaction_kind: str = self.interaction_kind

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "interaction_id": interaction_id,
                "state": state,
                "interaction_kind": interaction_kind,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        interaction_id = d.pop("interaction_id")

        state = check_agent_interaction_state(d.pop("state"))

        interaction_kind = check_agent_interaction_kind(d.pop("interaction_kind"))

        executor_interaction_update_interaction_update = cls(
            interaction_id=interaction_id,
            state=state,
            interaction_kind=interaction_kind,
        )

        return executor_interaction_update_interaction_update
