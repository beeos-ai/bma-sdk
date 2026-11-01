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
    from ..models.executor_event import ExecutorEvent
    from ..models.model_output_event import ModelOutputEvent
    from ..models.tool_result_event import ToolResultEvent


T = TypeVar("T", bound="CancelAgentResponse")


@_attrs_define
class CancelAgentResponse:
    """
    Attributes:
        event (Union['AgentInputEvent', 'ContextCheckpointEvent', 'ExecutorEvent', 'ModelOutputEvent',
            'ToolResultEvent', None]):
        runtime_cancel_requested (bool): Whether this request created or observed a durable runtime cancel request.
            Immediate delivery is best effort; runtime-lock renewal observes the durable request.
        affected (bool): Whether this request changed any cancelable work.
        actor_id (Union[Unset, str]):
    """

    event: Union[
        "AgentInputEvent",
        "ContextCheckpointEvent",
        "ExecutorEvent",
        "ModelOutputEvent",
        "ToolResultEvent",
        None,
    ]
    runtime_cancel_requested: bool
    affected: bool
    actor_id: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_input_event import AgentInputEvent
        from ..models.context_checkpoint_event import ContextCheckpointEvent
        from ..models.executor_event import ExecutorEvent
        from ..models.model_output_event import ModelOutputEvent
        from ..models.tool_result_event import ToolResultEvent

        event: Union[None, dict[str, Any]]
        if isinstance(self.event, AgentInputEvent):
            event = self.event.to_dict()
        elif isinstance(self.event, ModelOutputEvent):
            event = self.event.to_dict()
        elif isinstance(self.event, ToolResultEvent):
            event = self.event.to_dict()
        elif isinstance(self.event, ContextCheckpointEvent):
            event = self.event.to_dict()
        elif isinstance(self.event, ExecutorEvent):
            event = self.event.to_dict()
        else:
            event = self.event

        runtime_cancel_requested = self.runtime_cancel_requested

        affected = self.affected

        actor_id = self.actor_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "event": event,
                "runtime_cancel_requested": runtime_cancel_requested,
                "affected": affected,
            }
        )
        if actor_id is not UNSET:
            field_dict["actor_id"] = actor_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_input_event import AgentInputEvent
        from ..models.context_checkpoint_event import ContextCheckpointEvent
        from ..models.executor_event import ExecutorEvent
        from ..models.model_output_event import ModelOutputEvent
        from ..models.tool_result_event import ToolResultEvent

        d = dict(src_dict)

        def _parse_event(
            data: object,
        ) -> Union[
            "AgentInputEvent",
            "ContextCheckpointEvent",
            "ExecutorEvent",
            "ModelOutputEvent",
            "ToolResultEvent",
            None,
        ]:
            if data is None:
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
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_type_3 = ContextCheckpointEvent.from_dict(
                    data
                )

                return componentsschemas_agent_event_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_event_type_4 = ExecutorEvent.from_dict(data)

                return componentsschemas_agent_event_type_4
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "AgentInputEvent",
                    "ContextCheckpointEvent",
                    "ExecutorEvent",
                    "ModelOutputEvent",
                    "ToolResultEvent",
                    None,
                ],
                data,
            )

        event = _parse_event(d.pop("event"))

        runtime_cancel_requested = d.pop("runtime_cancel_requested")

        affected = d.pop("affected")

        actor_id = d.pop("actor_id", UNSET)

        cancel_agent_response = cls(
            event=event,
            runtime_cancel_requested=runtime_cancel_requested,
            affected=affected,
            actor_id=actor_id,
        )

        return cancel_agent_response
