import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.context_checkpoint_event_event_kind import (
    ContextCheckpointEventEventKind,
    check_context_checkpoint_event_event_kind,
)

T = TypeVar("T", bound="ContextCheckpointEvent")


@_attrs_define
class ContextCheckpointEvent:
    """
    Attributes:
        id (str):
        org_id (str):
        project_id (str): Project ID (proj_...).
        agent_id (str):
        turn_id (str):
        turn_sequence (int): Positive per-agent event, turn, or live-frame sequence.
        is_opening_event (bool):
        sequence (int): Positive per-agent event, turn, or live-frame sequence.
        event_kind (ContextCheckpointEventEventKind):
        context_checkpoint_id (str):
        summarized_through_event_sequence (int): Positive per-agent event, turn, or live-frame sequence.
        summary (str):
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
    event_kind: ContextCheckpointEventEventKind
    context_checkpoint_id: str
    summarized_through_event_sequence: int
    summary: str
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

        context_checkpoint_id = self.context_checkpoint_id

        summarized_through_event_sequence = self.summarized_through_event_sequence

        summary = self.summary

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
                "context_checkpoint_id": context_checkpoint_id,
                "summarized_through_event_sequence": summarized_through_event_sequence,
                "summary": summary,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        agent_id = d.pop("agent_id")

        turn_id = d.pop("turn_id")

        turn_sequence = d.pop("turn_sequence")

        is_opening_event = d.pop("is_opening_event")

        sequence = d.pop("sequence")

        event_kind = check_context_checkpoint_event_event_kind(d.pop("event_kind"))

        context_checkpoint_id = d.pop("context_checkpoint_id")

        summarized_through_event_sequence = d.pop("summarized_through_event_sequence")

        summary = d.pop("summary")

        created_at = isoparse(d.pop("created_at"))

        context_checkpoint_event = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            turn_id=turn_id,
            turn_sequence=turn_sequence,
            is_opening_event=is_opening_event,
            sequence=sequence,
            event_kind=event_kind,
            context_checkpoint_id=context_checkpoint_id,
            summarized_through_event_sequence=summarized_through_event_sequence,
            summary=summary,
            created_at=created_at,
        )

        return context_checkpoint_event
