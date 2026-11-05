from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.agent_interaction_state import (
    AgentInteractionState,
    check_agent_interaction_state,
)
from ..models.executor_interaction_update_type import (
    ExecutorInteractionUpdateType,
    check_executor_interaction_update_type,
)

if TYPE_CHECKING:
    from ..models.executor_interaction_update_interaction_update import (
        ExecutorInteractionUpdateInteractionUpdate,
    )


T = TypeVar("T", bound="ExecutorInteractionUpdate")


@_attrs_define
class ExecutorInteractionUpdate:
    """Best-effort stream frame of an agent executor session: an executor interaction (permission or question) opened or
    closed. tool_call_id is the agent.tool_use event ID for permissions and the interaction ID otherwise.

        Attributes:
            type_ (ExecutorInteractionUpdateType):
            session_id (str):
            tool_call_id (str):
            state (AgentInteractionState):
            interaction_update (ExecutorInteractionUpdateInteractionUpdate):
    """

    type_: ExecutorInteractionUpdateType
    session_id: str
    tool_call_id: str
    state: AgentInteractionState
    interaction_update: "ExecutorInteractionUpdateInteractionUpdate"

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        session_id = self.session_id

        tool_call_id = self.tool_call_id

        state: str = self.state

        interaction_update = self.interaction_update.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "session_id": session_id,
                "tool_call_id": tool_call_id,
                "state": state,
                "interaction_update": interaction_update,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.executor_interaction_update_interaction_update import (
            ExecutorInteractionUpdateInteractionUpdate,
        )

        d = dict(src_dict)
        type_ = check_executor_interaction_update_type(d.pop("type"))

        session_id = d.pop("session_id")

        tool_call_id = d.pop("tool_call_id")

        state = check_agent_interaction_state(d.pop("state"))

        interaction_update = ExecutorInteractionUpdateInteractionUpdate.from_dict(
            d.pop("interaction_update")
        )

        executor_interaction_update = cls(
            type_=type_,
            session_id=session_id,
            tool_call_id=tool_call_id,
            state=state,
            interaction_update=interaction_update,
        )

        return executor_interaction_update
