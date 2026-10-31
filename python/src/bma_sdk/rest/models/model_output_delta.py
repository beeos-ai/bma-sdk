from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.model_output_block_start_delta import ModelOutputBlockStartDelta
    from ..models.model_output_block_stop_delta import ModelOutputBlockStopDelta
    from ..models.model_output_error_delta import ModelOutputErrorDelta
    from ..models.model_output_message_stop_delta import ModelOutputMessageStopDelta
    from ..models.model_output_text_delta import ModelOutputTextDelta
    from ..models.model_output_thinking_delta import ModelOutputThinkingDelta
    from ..models.model_output_tool_arguments_delta import ModelOutputToolArgumentsDelta


T = TypeVar("T", bound="ModelOutputDelta")


@_attrs_define
class ModelOutputDelta:
    """
    Attributes:
        turn_id (str):
        model_call_context_id (str):
        seq (int): Positive per-agent event, turn, or live-frame sequence.
        source_seq_start (int): Positive per-agent event, turn, or live-frame sequence.
        source_seq_end (int): Positive per-agent event, turn, or live-frame sequence.
        coalesced_count (int): Positive count within an agent timeline.
        event (Union['ModelOutputBlockStartDelta', 'ModelOutputBlockStopDelta', 'ModelOutputErrorDelta',
            'ModelOutputMessageStopDelta', 'ModelOutputTextDelta', 'ModelOutputThinkingDelta',
            'ModelOutputToolArgumentsDelta']):
    """

    turn_id: str
    model_call_context_id: str
    seq: int
    source_seq_start: int
    source_seq_end: int
    coalesced_count: int
    event: Union[
        "ModelOutputBlockStartDelta",
        "ModelOutputBlockStopDelta",
        "ModelOutputErrorDelta",
        "ModelOutputMessageStopDelta",
        "ModelOutputTextDelta",
        "ModelOutputThinkingDelta",
        "ModelOutputToolArgumentsDelta",
    ]

    def to_dict(self) -> dict[str, Any]:
        from ..models.model_output_block_start_delta import ModelOutputBlockStartDelta
        from ..models.model_output_block_stop_delta import ModelOutputBlockStopDelta
        from ..models.model_output_message_stop_delta import ModelOutputMessageStopDelta
        from ..models.model_output_text_delta import ModelOutputTextDelta
        from ..models.model_output_thinking_delta import ModelOutputThinkingDelta
        from ..models.model_output_tool_arguments_delta import (
            ModelOutputToolArgumentsDelta,
        )

        turn_id = self.turn_id

        model_call_context_id = self.model_call_context_id

        seq = self.seq

        source_seq_start = self.source_seq_start

        source_seq_end = self.source_seq_end

        coalesced_count = self.coalesced_count

        event: dict[str, Any]
        if isinstance(self.event, ModelOutputBlockStartDelta):
            event = self.event.to_dict()
        elif isinstance(self.event, ModelOutputTextDelta):
            event = self.event.to_dict()
        elif isinstance(self.event, ModelOutputThinkingDelta):
            event = self.event.to_dict()
        elif isinstance(self.event, ModelOutputToolArgumentsDelta):
            event = self.event.to_dict()
        elif isinstance(self.event, ModelOutputBlockStopDelta):
            event = self.event.to_dict()
        elif isinstance(self.event, ModelOutputMessageStopDelta):
            event = self.event.to_dict()
        else:
            event = self.event.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "turn_id": turn_id,
                "model_call_context_id": model_call_context_id,
                "seq": seq,
                "source_seq_start": source_seq_start,
                "source_seq_end": source_seq_end,
                "coalesced_count": coalesced_count,
                "event": event,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_output_block_start_delta import ModelOutputBlockStartDelta
        from ..models.model_output_block_stop_delta import ModelOutputBlockStopDelta
        from ..models.model_output_error_delta import ModelOutputErrorDelta
        from ..models.model_output_message_stop_delta import ModelOutputMessageStopDelta
        from ..models.model_output_text_delta import ModelOutputTextDelta
        from ..models.model_output_thinking_delta import ModelOutputThinkingDelta
        from ..models.model_output_tool_arguments_delta import (
            ModelOutputToolArgumentsDelta,
        )

        d = dict(src_dict)
        turn_id = d.pop("turn_id")

        model_call_context_id = d.pop("model_call_context_id")

        seq = d.pop("seq")

        source_seq_start = d.pop("source_seq_start")

        source_seq_end = d.pop("source_seq_end")

        coalesced_count = d.pop("coalesced_count")

        def _parse_event(
            data: object,
        ) -> Union[
            "ModelOutputBlockStartDelta",
            "ModelOutputBlockStopDelta",
            "ModelOutputErrorDelta",
            "ModelOutputMessageStopDelta",
            "ModelOutputTextDelta",
            "ModelOutputThinkingDelta",
            "ModelOutputToolArgumentsDelta",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_model_output_stream_delta_type_0 = (
                    ModelOutputBlockStartDelta.from_dict(data)
                )

                return componentsschemas_model_output_stream_delta_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_model_output_stream_delta_type_1 = (
                    ModelOutputTextDelta.from_dict(data)
                )

                return componentsschemas_model_output_stream_delta_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_model_output_stream_delta_type_2 = (
                    ModelOutputThinkingDelta.from_dict(data)
                )

                return componentsschemas_model_output_stream_delta_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_model_output_stream_delta_type_3 = (
                    ModelOutputToolArgumentsDelta.from_dict(data)
                )

                return componentsschemas_model_output_stream_delta_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_model_output_stream_delta_type_4 = (
                    ModelOutputBlockStopDelta.from_dict(data)
                )

                return componentsschemas_model_output_stream_delta_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_model_output_stream_delta_type_5 = (
                    ModelOutputMessageStopDelta.from_dict(data)
                )

                return componentsschemas_model_output_stream_delta_type_5
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_model_output_stream_delta_type_6 = (
                ModelOutputErrorDelta.from_dict(data)
            )

            return componentsschemas_model_output_stream_delta_type_6

        event = _parse_event(d.pop("event"))

        model_output_delta = cls(
            turn_id=turn_id,
            model_call_context_id=model_call_context_id,
            seq=seq,
            source_seq_start=source_seq_start,
            source_seq_end=source_seq_end,
            coalesced_count=coalesced_count,
            event=event,
        )

        return model_output_delta
