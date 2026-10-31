from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.submit_tool_call_result_request_outcome import (
    SubmitToolCallResultRequestOutcome,
    check_submit_tool_call_result_request_outcome,
)

if TYPE_CHECKING:
    from ..models.inline_media_content_block import InlineMediaContentBlock
    from ..models.structured_data_content_block import StructuredDataContentBlock
    from ..models.text_content_block import TextContentBlock


T = TypeVar("T", bound="SubmitToolCallResultRequest")


@_attrs_define
class SubmitToolCallResultRequest:
    """
    Attributes:
        outcome (SubmitToolCallResultRequestOutcome): Whether the custom tool call succeeded or failed.
        content_blocks (list[Union['InlineMediaContentBlock', 'StructuredDataContentBlock', 'TextContentBlock']]): At
            most 20 inline media blocks per submission, each holding up to 10 MiB of decoded media and up to 24 MiB decoded
            across the submission. Non-media blocks may hold up to 1 MiB combined. The whole request body is capped at 48
            MiB.
    """

    outcome: SubmitToolCallResultRequestOutcome
    content_blocks: list[
        Union[
            "InlineMediaContentBlock", "StructuredDataContentBlock", "TextContentBlock"
        ]
    ]

    def to_dict(self) -> dict[str, Any]:
        from ..models.inline_media_content_block import InlineMediaContentBlock
        from ..models.text_content_block import TextContentBlock

        outcome: str = self.outcome

        content_blocks = []
        for content_blocks_item_data in self.content_blocks:
            content_blocks_item: dict[str, Any]
            if isinstance(content_blocks_item_data, TextContentBlock):
                content_blocks_item = content_blocks_item_data.to_dict()
            elif isinstance(content_blocks_item_data, InlineMediaContentBlock):
                content_blocks_item = content_blocks_item_data.to_dict()
            else:
                content_blocks_item = content_blocks_item_data.to_dict()

            content_blocks.append(content_blocks_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "outcome": outcome,
                "content_blocks": content_blocks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.inline_media_content_block import InlineMediaContentBlock
        from ..models.structured_data_content_block import StructuredDataContentBlock
        from ..models.text_content_block import TextContentBlock

        d = dict(src_dict)
        outcome = check_submit_tool_call_result_request_outcome(d.pop("outcome"))

        content_blocks = []
        _content_blocks = d.pop("content_blocks")
        for content_blocks_item_data in _content_blocks:

            def _parse_content_blocks_item(
                data: object,
            ) -> Union[
                "InlineMediaContentBlock",
                "StructuredDataContentBlock",
                "TextContentBlock",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_submit_tool_result_content_block_type_0 = (
                        TextContentBlock.from_dict(data)
                    )

                    return componentsschemas_submit_tool_result_content_block_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_submit_tool_result_content_block_type_1 = (
                        InlineMediaContentBlock.from_dict(data)
                    )

                    return componentsschemas_submit_tool_result_content_block_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_submit_tool_result_content_block_type_2 = (
                    StructuredDataContentBlock.from_dict(data)
                )

                return componentsschemas_submit_tool_result_content_block_type_2

            content_blocks_item = _parse_content_blocks_item(content_blocks_item_data)

            content_blocks.append(content_blocks_item)

        submit_tool_call_result_request = cls(
            outcome=outcome,
            content_blocks=content_blocks,
        )

        return submit_tool_call_result_request
