from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.agent_event_delta_type import (
    AgentEventDeltaType,
    check_agent_event_delta_type,
)

T = TypeVar("T", bound="AgentEventDelta")


@_attrs_define
class AgentEventDelta:
    """Best-effort preview frame of an agent executor session, sent only with stream_deltas: text appended to content block
    `index` of the executor event `event_id` before the durable executor_event arrives.

        Attributes:
            type_ (AgentEventDeltaType):
            session_id (str):
            turn_id (str):
            event_id (str):
            event_type (str):
            index (int):
            text (str):
    """

    type_: AgentEventDeltaType
    session_id: str
    turn_id: str
    event_id: str
    event_type: str
    index: int
    text: str

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        session_id = self.session_id

        turn_id = self.turn_id

        event_id = self.event_id

        event_type = self.event_type

        index = self.index

        text = self.text

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "session_id": session_id,
                "turn_id": turn_id,
                "event_id": event_id,
                "event_type": event_type,
                "index": index,
                "text": text,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_agent_event_delta_type(d.pop("type"))

        session_id = d.pop("session_id")

        turn_id = d.pop("turn_id")

        event_id = d.pop("event_id")

        event_type = d.pop("event_type")

        index = d.pop("index")

        text = d.pop("text")

        agent_event_delta = cls(
            type_=type_,
            session_id=session_id,
            turn_id=turn_id,
            event_id=event_id,
            event_type=event_type,
            index=index,
            text=text,
        )

        return agent_event_delta
