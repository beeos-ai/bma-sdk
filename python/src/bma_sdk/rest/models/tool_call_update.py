from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.tool_call_state import ToolCallState, check_tool_call_state
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_interaction_update import AgentInteractionUpdate


T = TypeVar("T", bound="ToolCallUpdate")


@_attrs_define
class ToolCallUpdate:
    """A notification that a tool call entered a lifecycle state. On the event stream, this is ephemeral and sent for the
    streamed agent and every subagent beneath it, so questions, permission requests, and custom tool calls anywhere in
    the tree surface here; query the list endpoints with `include_subagents` for the current rows.

        Attributes:
            tool_call_id (str):
            state (ToolCallState): Current lifecycle state. awaiting_authorization has not evaluated its permission mode;
                awaiting_permission has an open authorization prompt; ready is authorized and eligible to run; running has an
                active worker; waiting has durable work that will complete the call independently; completed is terminal and
                includes outcome and completed_at. Custom calls remain ready until a consumer submits their result.
            agent_id (Union[Unset, str]):
            interaction_update (Union[Unset, AgentInteractionUpdate]):
    """

    tool_call_id: str
    state: ToolCallState
    agent_id: Union[Unset, str] = UNSET
    interaction_update: Union[Unset, "AgentInteractionUpdate"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        tool_call_id = self.tool_call_id

        state: str = self.state

        agent_id = self.agent_id

        interaction_update: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.interaction_update, Unset):
            interaction_update = self.interaction_update.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "tool_call_id": tool_call_id,
                "state": state,
            }
        )
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if interaction_update is not UNSET:
            field_dict["interaction_update"] = interaction_update

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_interaction_update import AgentInteractionUpdate

        d = dict(src_dict)
        tool_call_id = d.pop("tool_call_id")

        state = check_tool_call_state(d.pop("state"))

        agent_id = d.pop("agent_id", UNSET)

        _interaction_update = d.pop("interaction_update", UNSET)
        interaction_update: Union[Unset, AgentInteractionUpdate]
        if isinstance(_interaction_update, Unset):
            interaction_update = UNSET
        else:
            interaction_update = AgentInteractionUpdate.from_dict(_interaction_update)

        tool_call_update = cls(
            tool_call_id=tool_call_id,
            state=state,
            agent_id=agent_id,
            interaction_update=interaction_update,
        )

        return tool_call_update
