from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.agent_input_event import AgentInputEvent
    from ..models.context_checkpoint_event import ContextCheckpointEvent
    from ..models.executor_event import ExecutorEvent
    from ..models.model_output_event import ModelOutputEvent
    from ..models.tool_result_event import ToolResultEvent


T = TypeVar("T", bound="ListTurnEventsResponse")


@_attrs_define
class ListTurnEventsResponse:
    """
    Attributes:
        data (list[Union['AgentInputEvent', 'ContextCheckpointEvent', 'ExecutorEvent', 'ModelOutputEvent',
            'ToolResultEvent']]):
        next_before_sequence (Union[None, int]): Pass this value as before_sequence to fetch older events, or null when
            this page reached the beginning of the turn.
    """

    data: list[
        Union[
            "AgentInputEvent",
            "ContextCheckpointEvent",
            "ExecutorEvent",
            "ModelOutputEvent",
            "ToolResultEvent",
        ]
    ]
    next_before_sequence: Union[None, int]

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_input_event import AgentInputEvent
        from ..models.context_checkpoint_event import ContextCheckpointEvent
        from ..models.model_output_event import ModelOutputEvent
        from ..models.tool_result_event import ToolResultEvent

        data = []
        for data_item_data in self.data:
            data_item: dict[str, Any]
            if isinstance(data_item_data, AgentInputEvent):
                data_item = data_item_data.to_dict()
            elif isinstance(data_item_data, ModelOutputEvent):
                data_item = data_item_data.to_dict()
            elif isinstance(data_item_data, ToolResultEvent):
                data_item = data_item_data.to_dict()
            elif isinstance(data_item_data, ContextCheckpointEvent):
                data_item = data_item_data.to_dict()
            else:
                data_item = data_item_data.to_dict()

            data.append(data_item)

        next_before_sequence: Union[None, int]
        next_before_sequence = self.next_before_sequence

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
                "next_before_sequence": next_before_sequence,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_input_event import AgentInputEvent
        from ..models.context_checkpoint_event import ContextCheckpointEvent
        from ..models.executor_event import ExecutorEvent
        from ..models.model_output_event import ModelOutputEvent
        from ..models.tool_result_event import ToolResultEvent

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:

            def _parse_data_item(
                data: object,
            ) -> Union[
                "AgentInputEvent",
                "ContextCheckpointEvent",
                "ExecutorEvent",
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
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_agent_event_type_3 = (
                        ContextCheckpointEvent.from_dict(data)
                    )

                    return componentsschemas_agent_event_type_3
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_type_4 = ExecutorEvent.from_dict(data)

                return componentsschemas_agent_event_type_4

            data_item = _parse_data_item(data_item_data)

            data.append(data_item)

        def _parse_next_before_sequence(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        next_before_sequence = _parse_next_before_sequence(
            d.pop("next_before_sequence")
        )

        list_turn_events_response = cls(
            data=data,
            next_before_sequence=next_before_sequence,
        )

        return list_turn_events_response
