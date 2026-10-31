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

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_input_event import AgentInputEvent
    from ..models.context_checkpoint_event import ContextCheckpointEvent
    from ..models.model_output_event import ModelOutputEvent
    from ..models.tool_result_event import ToolResultEvent


T = TypeVar("T", bound="AgentTurn")


@_attrs_define
class AgentTurn:
    """
    Attributes:
        id (str):
        agent_id (str):
        turn_sequence (int): Positive per-agent event, turn, or live-frame sequence.
        event_count (int): Positive count within an agent timeline.
        opening_events (list[Union['AgentInputEvent', 'ContextCheckpointEvent', 'ModelOutputEvent',
            'ToolResultEvent']]):
        started_at (datetime.datetime):
        updated_at (datetime.datetime):
        latest_event (Union['AgentInputEvent', 'ContextCheckpointEvent', 'ModelOutputEvent', 'ToolResultEvent', Unset]):
        latest_semantic_event (Union['AgentInputEvent', 'ContextCheckpointEvent', 'ModelOutputEvent', 'ToolResultEvent',
            Unset]):
    """

    id: str
    agent_id: str
    turn_sequence: int
    event_count: int
    opening_events: list[
        Union[
            "AgentInputEvent",
            "ContextCheckpointEvent",
            "ModelOutputEvent",
            "ToolResultEvent",
        ]
    ]
    started_at: datetime.datetime
    updated_at: datetime.datetime
    latest_event: Union[
        "AgentInputEvent",
        "ContextCheckpointEvent",
        "ModelOutputEvent",
        "ToolResultEvent",
        Unset,
    ] = UNSET
    latest_semantic_event: Union[
        "AgentInputEvent",
        "ContextCheckpointEvent",
        "ModelOutputEvent",
        "ToolResultEvent",
        Unset,
    ] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_input_event import AgentInputEvent
        from ..models.model_output_event import ModelOutputEvent
        from ..models.tool_result_event import ToolResultEvent

        id = self.id

        agent_id = self.agent_id

        turn_sequence = self.turn_sequence

        event_count = self.event_count

        opening_events = []
        for opening_events_item_data in self.opening_events:
            opening_events_item: dict[str, Any]
            if isinstance(opening_events_item_data, AgentInputEvent):
                opening_events_item = opening_events_item_data.to_dict()
            elif isinstance(opening_events_item_data, ModelOutputEvent):
                opening_events_item = opening_events_item_data.to_dict()
            elif isinstance(opening_events_item_data, ToolResultEvent):
                opening_events_item = opening_events_item_data.to_dict()
            else:
                opening_events_item = opening_events_item_data.to_dict()

            opening_events.append(opening_events_item)

        started_at = self.started_at.isoformat()

        updated_at = self.updated_at.isoformat()

        latest_event: Union[Unset, dict[str, Any]]
        if isinstance(self.latest_event, Unset):
            latest_event = UNSET
        elif isinstance(self.latest_event, AgentInputEvent):
            latest_event = self.latest_event.to_dict()
        elif isinstance(self.latest_event, ModelOutputEvent):
            latest_event = self.latest_event.to_dict()
        elif isinstance(self.latest_event, ToolResultEvent):
            latest_event = self.latest_event.to_dict()
        else:
            latest_event = self.latest_event.to_dict()

        latest_semantic_event: Union[Unset, dict[str, Any]]
        if isinstance(self.latest_semantic_event, Unset):
            latest_semantic_event = UNSET
        elif isinstance(self.latest_semantic_event, AgentInputEvent):
            latest_semantic_event = self.latest_semantic_event.to_dict()
        elif isinstance(self.latest_semantic_event, ModelOutputEvent):
            latest_semantic_event = self.latest_semantic_event.to_dict()
        elif isinstance(self.latest_semantic_event, ToolResultEvent):
            latest_semantic_event = self.latest_semantic_event.to_dict()
        else:
            latest_semantic_event = self.latest_semantic_event.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "agent_id": agent_id,
                "turn_sequence": turn_sequence,
                "event_count": event_count,
                "opening_events": opening_events,
                "started_at": started_at,
                "updated_at": updated_at,
            }
        )
        if latest_event is not UNSET:
            field_dict["latest_event"] = latest_event
        if latest_semantic_event is not UNSET:
            field_dict["latest_semantic_event"] = latest_semantic_event

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_input_event import AgentInputEvent
        from ..models.context_checkpoint_event import ContextCheckpointEvent
        from ..models.model_output_event import ModelOutputEvent
        from ..models.tool_result_event import ToolResultEvent

        d = dict(src_dict)
        id = d.pop("id")

        agent_id = d.pop("agent_id")

        turn_sequence = d.pop("turn_sequence")

        event_count = d.pop("event_count")

        opening_events = []
        _opening_events = d.pop("opening_events")
        for opening_events_item_data in _opening_events:

            def _parse_opening_events_item(
                data: object,
            ) -> Union[
                "AgentInputEvent",
                "ContextCheckpointEvent",
                "ModelOutputEvent",
                "ToolResultEvent",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_agent_event_type_0 = AgentInputEvent.from_dict(
                        data
                    )

                    return componentsschemas_agent_event_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_agent_event_type_1 = ModelOutputEvent.from_dict(
                        data
                    )

                    return componentsschemas_agent_event_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_agent_event_type_2 = ToolResultEvent.from_dict(
                        data
                    )

                    return componentsschemas_agent_event_type_2
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_type_3 = ContextCheckpointEvent.from_dict(
                    data
                )

                return componentsschemas_agent_event_type_3

            opening_events_item = _parse_opening_events_item(opening_events_item_data)

            opening_events.append(opening_events_item)

        started_at = isoparse(d.pop("started_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_latest_event(
            data: object,
        ) -> Union[
            "AgentInputEvent",
            "ContextCheckpointEvent",
            "ModelOutputEvent",
            "ToolResultEvent",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_type_0 = AgentInputEvent.from_dict(data)

                return componentsschemas_agent_event_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_type_1 = ModelOutputEvent.from_dict(data)

                return componentsschemas_agent_event_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_type_2 = ToolResultEvent.from_dict(data)

                return componentsschemas_agent_event_type_2
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_agent_event_type_3 = ContextCheckpointEvent.from_dict(
                data
            )

            return componentsschemas_agent_event_type_3

        latest_event = _parse_latest_event(d.pop("latest_event", UNSET))

        def _parse_latest_semantic_event(
            data: object,
        ) -> Union[
            "AgentInputEvent",
            "ContextCheckpointEvent",
            "ModelOutputEvent",
            "ToolResultEvent",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_type_0 = AgentInputEvent.from_dict(data)

                return componentsschemas_agent_event_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_type_1 = ModelOutputEvent.from_dict(data)

                return componentsschemas_agent_event_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_type_2 = ToolResultEvent.from_dict(data)

                return componentsschemas_agent_event_type_2
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_agent_event_type_3 = ContextCheckpointEvent.from_dict(
                data
            )

            return componentsschemas_agent_event_type_3

        latest_semantic_event = _parse_latest_semantic_event(
            d.pop("latest_semantic_event", UNSET)
        )

        agent_turn = cls(
            id=id,
            agent_id=agent_id,
            turn_sequence=turn_sequence,
            event_count=event_count,
            opening_events=opening_events,
            started_at=started_at,
            updated_at=updated_at,
            latest_event=latest_event,
            latest_semantic_event=latest_semantic_event,
        )

        return agent_turn
