import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.tool_call_outcome import ToolCallOutcome, check_tool_call_outcome
from ..models.tool_call_state import ToolCallState, check_tool_call_state
from ..models.tool_call_type import ToolCallType, check_tool_call_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tool_input import ToolInput


T = TypeVar("T", bound="ToolCall")


@_attrs_define
class ToolCall:
    """A model-emitted tool call together with its current lifecycle state.

    Attributes:
        id (str):
        agent_id (str):
        turn_id (str):
        provider_call_id (str):
        name (str):
        input_ (ToolInput): Non-null JSON object containing the arguments emitted for a tool call.
        type_ (ToolCallType): Identifies who manages execution. Built-in and MCP calls are platform-managed; custom
            calls wait for an external consumer to submit their result.
        state (ToolCallState): Current lifecycle state. awaiting_authorization has not evaluated its permission mode;
            awaiting_permission has an open authorization prompt; ready is authorized and eligible to run; running has an
            active worker; waiting has durable work that will complete the call independently; completed is terminal and
            includes outcome and completed_at. Custom calls remain ready until a consumer submits their result.
        created_at (datetime.datetime):
        outcome (Union[Unset, ToolCallOutcome]): Terminal outcome, present only when state is completed.
        completed_at (Union[Unset, datetime.datetime]):
    """

    id: str
    agent_id: str
    turn_id: str
    provider_call_id: str
    name: str
    input_: "ToolInput"
    type_: ToolCallType
    state: ToolCallState
    created_at: datetime.datetime
    outcome: Union[Unset, ToolCallOutcome] = UNSET
    completed_at: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        agent_id = self.agent_id

        turn_id = self.turn_id

        provider_call_id = self.provider_call_id

        name = self.name

        input_ = self.input_.to_dict()

        type_: str = self.type_

        state: str = self.state

        created_at = self.created_at.isoformat()

        outcome: Union[Unset, str] = UNSET
        if not isinstance(self.outcome, Unset):
            outcome = self.outcome

        completed_at: Union[Unset, str] = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "agent_id": agent_id,
                "turn_id": turn_id,
                "provider_call_id": provider_call_id,
                "name": name,
                "input": input_,
                "type": type_,
                "state": state,
                "created_at": created_at,
            }
        )
        if outcome is not UNSET:
            field_dict["outcome"] = outcome
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tool_input import ToolInput

        d = dict(src_dict)
        id = d.pop("id")

        agent_id = d.pop("agent_id")

        turn_id = d.pop("turn_id")

        provider_call_id = d.pop("provider_call_id")

        name = d.pop("name")

        input_ = ToolInput.from_dict(d.pop("input"))

        type_ = check_tool_call_type(d.pop("type"))

        state = check_tool_call_state(d.pop("state"))

        created_at = isoparse(d.pop("created_at"))

        _outcome = d.pop("outcome", UNSET)
        outcome: Union[Unset, ToolCallOutcome]
        if isinstance(_outcome, Unset):
            outcome = UNSET
        else:
            outcome = check_tool_call_outcome(_outcome)

        _completed_at = d.pop("completed_at", UNSET)
        completed_at: Union[Unset, datetime.datetime]
        if isinstance(_completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = isoparse(_completed_at)

        tool_call = cls(
            id=id,
            agent_id=agent_id,
            turn_id=turn_id,
            provider_call_id=provider_call_id,
            name=name,
            input_=input_,
            type_=type_,
            state=state,
            created_at=created_at,
            outcome=outcome,
            completed_at=completed_at,
        )

        return tool_call
