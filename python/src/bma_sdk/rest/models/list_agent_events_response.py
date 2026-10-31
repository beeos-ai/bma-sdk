from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_input_event import AgentInputEvent
    from ..models.context_checkpoint_event import ContextCheckpointEvent
    from ..models.model_output_event import ModelOutputEvent
    from ..models.tool_result_event import ToolResultEvent


T = TypeVar("T", bound="ListAgentEventsResponse")


@_attrs_define
class ListAgentEventsResponse:
    """
    Attributes:
        data (list[Union['AgentInputEvent', 'ContextCheckpointEvent', 'ModelOutputEvent', 'ToolResultEvent']]):
        next_after_sequence (int): Non-negative agent timeline cursor.
        has_more (bool): True when another immediate request in the requested pagination direction can return more
            currently available events.
        next_before_sequence (Union[None, Unset, int]): Sequence to pass as before_sequence for the next older page.
            Null when no older events remain or when paginating forward.
    """

    data: list[
        Union[
            "AgentInputEvent",
            "ContextCheckpointEvent",
            "ModelOutputEvent",
            "ToolResultEvent",
        ]
    ]
    next_after_sequence: int
    has_more: bool
    next_before_sequence: Union[None, Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_input_event import AgentInputEvent
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
            else:
                data_item = data_item_data.to_dict()

            data.append(data_item)

        next_after_sequence = self.next_after_sequence

        has_more = self.has_more

        next_before_sequence: Union[None, Unset, int]
        if isinstance(self.next_before_sequence, Unset):
            next_before_sequence = UNSET
        else:
            next_before_sequence = self.next_before_sequence

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
                "next_after_sequence": next_after_sequence,
                "has_more": has_more,
            }
        )
        if next_before_sequence is not UNSET:
            field_dict["next_before_sequence"] = next_before_sequence

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_input_event import AgentInputEvent
        from ..models.context_checkpoint_event import ContextCheckpointEvent
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

            data_item = _parse_data_item(data_item_data)

            data.append(data_item)

        next_after_sequence = d.pop("next_after_sequence")

        has_more = d.pop("has_more")

        def _parse_next_before_sequence(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        next_before_sequence = _parse_next_before_sequence(
            d.pop("next_before_sequence", UNSET)
        )

        list_agent_events_response = cls(
            data=data,
            next_after_sequence=next_after_sequence,
            has_more=has_more,
            next_before_sequence=next_before_sequence,
        )

        return list_agent_events_response
