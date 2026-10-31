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

if TYPE_CHECKING:
    from ..models.media_ref_content_block import MediaRefContentBlock
    from ..models.structured_data_content_block import StructuredDataContentBlock
    from ..models.text_content_block import TextContentBlock


T = TypeVar("T", bound="ToolResult")


@_attrs_define
class ToolResult:
    """
    Attributes:
        event_id (str):
        agent_id (str):
        tool_call_id (str):
        outcome (ToolCallOutcome): Terminal outcome, present only when state is completed.
        content_blocks (list[Union['MediaRefContentBlock', 'StructuredDataContentBlock', 'TextContentBlock']]):
        created_at (datetime.datetime):
    """

    event_id: str
    agent_id: str
    tool_call_id: str
    outcome: ToolCallOutcome
    content_blocks: list[
        Union["MediaRefContentBlock", "StructuredDataContentBlock", "TextContentBlock"]
    ]
    created_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        from ..models.media_ref_content_block import MediaRefContentBlock
        from ..models.text_content_block import TextContentBlock

        event_id = self.event_id

        agent_id = self.agent_id

        tool_call_id = self.tool_call_id

        outcome: str = self.outcome

        content_blocks = []
        for content_blocks_item_data in self.content_blocks:
            content_blocks_item: dict[str, Any]
            if isinstance(content_blocks_item_data, TextContentBlock):
                content_blocks_item = content_blocks_item_data.to_dict()
            elif isinstance(content_blocks_item_data, MediaRefContentBlock):
                content_blocks_item = content_blocks_item_data.to_dict()
            else:
                content_blocks_item = content_blocks_item_data.to_dict()

            content_blocks.append(content_blocks_item)

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "event_id": event_id,
                "agent_id": agent_id,
                "tool_call_id": tool_call_id,
                "outcome": outcome,
                "content_blocks": content_blocks,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.media_ref_content_block import MediaRefContentBlock
        from ..models.structured_data_content_block import StructuredDataContentBlock
        from ..models.text_content_block import TextContentBlock

        d = dict(src_dict)
        event_id = d.pop("event_id")

        agent_id = d.pop("agent_id")

        tool_call_id = d.pop("tool_call_id")

        outcome = check_tool_call_outcome(d.pop("outcome"))

        content_blocks = []
        _content_blocks = d.pop("content_blocks")
        for content_blocks_item_data in _content_blocks:

            def _parse_content_blocks_item(
                data: object,
            ) -> Union[
                "MediaRefContentBlock", "StructuredDataContentBlock", "TextContentBlock"
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_tool_result_content_block_type_0 = (
                        TextContentBlock.from_dict(data)
                    )

                    return componentsschemas_tool_result_content_block_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_tool_result_content_block_type_1 = (
                        MediaRefContentBlock.from_dict(data)
                    )

                    return componentsschemas_tool_result_content_block_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_tool_result_content_block_type_2 = (
                    StructuredDataContentBlock.from_dict(data)
                )

                return componentsschemas_tool_result_content_block_type_2

            content_blocks_item = _parse_content_blocks_item(content_blocks_item_data)

            content_blocks.append(content_blocks_item)

        created_at = isoparse(d.pop("created_at"))

        tool_result = cls(
            event_id=event_id,
            agent_id=agent_id,
            tool_call_id=tool_call_id,
            outcome=outcome,
            content_blocks=content_blocks,
            created_at=created_at,
        )

        return tool_result
