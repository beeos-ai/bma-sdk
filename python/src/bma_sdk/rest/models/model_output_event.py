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

from ..models.model_output_event_event_kind import (
    ModelOutputEventEventKind,
    check_model_output_event_event_kind,
)
from ..models.model_output_stop_reason import (
    ModelOutputStopReason,
    check_model_output_stop_reason,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.error_content_block import ErrorContentBlock
    from ..models.media_ref_content_block import MediaRefContentBlock
    from ..models.model_output_event_provider_metadata import (
        ModelOutputEventProviderMetadata,
    )
    from ..models.model_tool_call_content_block import ModelToolCallContentBlock
    from ..models.model_usage import ModelUsage
    from ..models.reasoning_content_block import ReasoningContentBlock
    from ..models.text_content_block import TextContentBlock


T = TypeVar("T", bound="ModelOutputEvent")


@_attrs_define
class ModelOutputEvent:
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
        event_kind (ModelOutputEventEventKind):
        model_call_context_id (str):
        stop_reason (ModelOutputStopReason): Stop reasons admitted as durable model-output events.
        content_blocks (list[Union['ErrorContentBlock', 'MediaRefContentBlock', 'ModelToolCallContentBlock',
            'ReasoningContentBlock', 'TextContentBlock']]):
        created_at (datetime.datetime):
        usage (Union[Unset, ModelUsage]): Token counts the provider reported for one model call. Cache and reasoning
            counts are omitted when the provider reported none.
        provider_metadata (Union[Unset, ModelOutputEventProviderMetadata]): Facts the provider reported about this call,
            keyed by provider (for example `openrouter.provider` names the upstream that served an OpenRouter request).
            Present only when the provider reported something.
    """

    id: str
    org_id: str
    project_id: str
    agent_id: str
    turn_id: str
    turn_sequence: int
    is_opening_event: bool
    sequence: int
    event_kind: ModelOutputEventEventKind
    model_call_context_id: str
    stop_reason: ModelOutputStopReason
    content_blocks: list[
        Union[
            "ErrorContentBlock",
            "MediaRefContentBlock",
            "ModelToolCallContentBlock",
            "ReasoningContentBlock",
            "TextContentBlock",
        ]
    ]
    created_at: datetime.datetime
    usage: Union[Unset, "ModelUsage"] = UNSET
    provider_metadata: Union[Unset, "ModelOutputEventProviderMetadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.media_ref_content_block import MediaRefContentBlock
        from ..models.model_tool_call_content_block import ModelToolCallContentBlock
        from ..models.reasoning_content_block import ReasoningContentBlock
        from ..models.text_content_block import TextContentBlock

        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        agent_id = self.agent_id

        turn_id = self.turn_id

        turn_sequence = self.turn_sequence

        is_opening_event = self.is_opening_event

        sequence = self.sequence

        event_kind: str = self.event_kind

        model_call_context_id = self.model_call_context_id

        stop_reason: str = self.stop_reason

        content_blocks = []
        for content_blocks_item_data in self.content_blocks:
            content_blocks_item: dict[str, Any]
            if isinstance(content_blocks_item_data, TextContentBlock):
                content_blocks_item = content_blocks_item_data.to_dict()
            elif isinstance(content_blocks_item_data, MediaRefContentBlock):
                content_blocks_item = content_blocks_item_data.to_dict()
            elif isinstance(content_blocks_item_data, ReasoningContentBlock):
                content_blocks_item = content_blocks_item_data.to_dict()
            elif isinstance(content_blocks_item_data, ModelToolCallContentBlock):
                content_blocks_item = content_blocks_item_data.to_dict()
            else:
                content_blocks_item = content_blocks_item_data.to_dict()

            content_blocks.append(content_blocks_item)

        created_at = self.created_at.isoformat()

        usage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()

        provider_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.provider_metadata, Unset):
            provider_metadata = self.provider_metadata.to_dict()

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
                "model_call_context_id": model_call_context_id,
                "stop_reason": stop_reason,
                "content_blocks": content_blocks,
                "created_at": created_at,
            }
        )
        if usage is not UNSET:
            field_dict["usage"] = usage
        if provider_metadata is not UNSET:
            field_dict["provider_metadata"] = provider_metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error_content_block import ErrorContentBlock
        from ..models.media_ref_content_block import MediaRefContentBlock
        from ..models.model_output_event_provider_metadata import (
            ModelOutputEventProviderMetadata,
        )
        from ..models.model_tool_call_content_block import ModelToolCallContentBlock
        from ..models.model_usage import ModelUsage
        from ..models.reasoning_content_block import ReasoningContentBlock
        from ..models.text_content_block import TextContentBlock

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        agent_id = d.pop("agent_id")

        turn_id = d.pop("turn_id")

        turn_sequence = d.pop("turn_sequence")

        is_opening_event = d.pop("is_opening_event")

        sequence = d.pop("sequence")

        event_kind = check_model_output_event_event_kind(d.pop("event_kind"))

        model_call_context_id = d.pop("model_call_context_id")

        stop_reason = check_model_output_stop_reason(d.pop("stop_reason"))

        content_blocks = []
        _content_blocks = d.pop("content_blocks")
        for content_blocks_item_data in _content_blocks:

            def _parse_content_blocks_item(
                data: object,
            ) -> Union[
                "ErrorContentBlock",
                "MediaRefContentBlock",
                "ModelToolCallContentBlock",
                "ReasoningContentBlock",
                "TextContentBlock",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_model_output_content_block_type_0 = (
                        TextContentBlock.from_dict(data)
                    )

                    return componentsschemas_model_output_content_block_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_model_output_content_block_type_1 = (
                        MediaRefContentBlock.from_dict(data)
                    )

                    return componentsschemas_model_output_content_block_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_model_output_content_block_type_2 = (
                        ReasoningContentBlock.from_dict(data)
                    )

                    return componentsschemas_model_output_content_block_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_model_output_content_block_type_3 = (
                        ModelToolCallContentBlock.from_dict(data)
                    )

                    return componentsschemas_model_output_content_block_type_3
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_model_output_content_block_type_4 = (
                    ErrorContentBlock.from_dict(data)
                )

                return componentsschemas_model_output_content_block_type_4

            content_blocks_item = _parse_content_blocks_item(content_blocks_item_data)

            content_blocks.append(content_blocks_item)

        created_at = isoparse(d.pop("created_at"))

        _usage = d.pop("usage", UNSET)
        usage: Union[Unset, ModelUsage]
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = ModelUsage.from_dict(_usage)

        _provider_metadata = d.pop("provider_metadata", UNSET)
        provider_metadata: Union[Unset, ModelOutputEventProviderMetadata]
        if isinstance(_provider_metadata, Unset):
            provider_metadata = UNSET
        else:
            provider_metadata = ModelOutputEventProviderMetadata.from_dict(
                _provider_metadata
            )

        model_output_event = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            turn_id=turn_id,
            turn_sequence=turn_sequence,
            is_opening_event=is_opening_event,
            sequence=sequence,
            event_kind=event_kind,
            model_call_context_id=model_call_context_id,
            stop_reason=stop_reason,
            content_blocks=content_blocks,
            created_at=created_at,
            usage=usage,
            provider_metadata=provider_metadata,
        )

        return model_output_event
