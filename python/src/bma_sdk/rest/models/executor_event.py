import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.executor_event_event_kind import (
    ExecutorEventEventKind,
    check_executor_event_event_kind,
)

if TYPE_CHECKING:
    from ..models.executor_event_event import ExecutorEventEvent


T = TypeVar("T", bound="ExecutorEvent")


@_attrs_define
class ExecutorEvent:
    """An Anthropic-shaped session event reported by an agent executor (Executor Protocol capability agent), or a
    user.tool_confirmation the platform wrote when an executor interaction was answered.

        Attributes:
            id (str):
            org_id (str):
            project_id (str): Project ID (proj_...).
            agent_id (str):
            turn_id (str):
            turn_sequence (int): Positive per-agent event, turn, or live-frame sequence.
            is_opening_event (bool):
            sequence (int): Positive per-agent event, turn, or live-frame sequence.
            event_kind (ExecutorEventEventKind):
            executor_event_id (str): Executor-assigned event id; agent.tool_result.tool_use_id refers to the agent.tool_use
                event by this id.
            event (ExecutorEventEvent): The event as reported, with its Anthropic type (agent.message, agent.tool_use,
                session.status_idle, ...).
            created_at (datetime.datetime):
    """

    id: str
    org_id: str
    project_id: str
    agent_id: str
    turn_id: str
    turn_sequence: int
    is_opening_event: bool
    sequence: int
    event_kind: ExecutorEventEventKind
    executor_event_id: str
    event: "ExecutorEventEvent"
    created_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        agent_id = self.agent_id

        turn_id = self.turn_id

        turn_sequence = self.turn_sequence

        is_opening_event = self.is_opening_event

        sequence = self.sequence

        event_kind: str = self.event_kind

        executor_event_id = self.executor_event_id

        event = self.event.to_dict()

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "agent_id": agent_id,
                "turn_id": turn_id,
                "turn_sequence": turn_sequence,
                "is_opening_event": is_opening_event,
                "sequence": sequence,
                "event_kind": event_kind,
                "executor_event_id": executor_event_id,
                "event": event,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.executor_event_event import ExecutorEventEvent

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        agent_id = d.pop("agent_id")

        turn_id = d.pop("turn_id")

        turn_sequence = d.pop("turn_sequence")

        is_opening_event = d.pop("is_opening_event")

        sequence = d.pop("sequence")

        event_kind = check_executor_event_event_kind(d.pop("event_kind"))

        executor_event_id = d.pop("executor_event_id")

        event = ExecutorEventEvent.from_dict(d.pop("event"))

        created_at = isoparse(d.pop("created_at"))

        executor_event = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            turn_id=turn_id,
            turn_sequence=turn_sequence,
            is_opening_event=is_opening_event,
            sequence=sequence,
            event_kind=event_kind,
            executor_event_id=executor_event_id,
            event=event,
            created_at=created_at,
        )

        return executor_event
