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

T = TypeVar("T", bound="AgentInteractionUpdate")


@_attrs_define
class AgentInteractionUpdate:
    """
    Attributes:
        id (str):
        interaction_kind (AgentInteractionKind):
        state (AgentInteractionState):
    """

    id: str
    interaction_kind: AgentInteractionKind
    state: AgentInteractionState

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        interaction_kind: str = self.interaction_kind

        state: str = self.state

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "interaction_kind": interaction_kind,
                "state": state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        interaction_kind = check_agent_interaction_kind(d.pop("interaction_kind"))

        state = check_agent_interaction_state(d.pop("state"))

        agent_interaction_update = cls(
            id=id,
            interaction_kind=interaction_kind,
            state=state,
        )

        return agent_interaction_update
