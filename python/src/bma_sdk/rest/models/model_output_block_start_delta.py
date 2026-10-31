from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.model_output_block_start_delta_kind import (
    ModelOutputBlockStartDeltaKind,
    check_model_output_block_start_delta_kind,
)

if TYPE_CHECKING:
    from ..models.model_output_text_stream_block import ModelOutputTextStreamBlock
    from ..models.model_output_thinking_stream_block import (
        ModelOutputThinkingStreamBlock,
    )
    from ..models.model_output_tool_use_stream_block import (
        ModelOutputToolUseStreamBlock,
    )


T = TypeVar("T", bound="ModelOutputBlockStartDelta")


@_attrs_define
class ModelOutputBlockStartDelta:
    """
    Attributes:
        kind (ModelOutputBlockStartDeltaKind):
        block_index (int):
        block (Union['ModelOutputTextStreamBlock', 'ModelOutputThinkingStreamBlock', 'ModelOutputToolUseStreamBlock']):
    """

    kind: ModelOutputBlockStartDeltaKind
    block_index: int
    block: Union[
        "ModelOutputTextStreamBlock",
        "ModelOutputThinkingStreamBlock",
        "ModelOutputToolUseStreamBlock",
    ]

    def to_dict(self) -> dict[str, Any]:
        from ..models.model_output_text_stream_block import ModelOutputTextStreamBlock
        from ..models.model_output_thinking_stream_block import (
            ModelOutputThinkingStreamBlock,
        )

        kind: str = self.kind

        block_index = self.block_index

        block: dict[str, Any]
        if isinstance(self.block, ModelOutputTextStreamBlock):
            block = self.block.to_dict()
        elif isinstance(self.block, ModelOutputThinkingStreamBlock):
            block = self.block.to_dict()
        else:
            block = self.block.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "block_index": block_index,
                "block": block,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_output_text_stream_block import ModelOutputTextStreamBlock
        from ..models.model_output_thinking_stream_block import (
            ModelOutputThinkingStreamBlock,
        )
        from ..models.model_output_tool_use_stream_block import (
            ModelOutputToolUseStreamBlock,
        )

        d = dict(src_dict)
        kind = check_model_output_block_start_delta_kind(d.pop("kind"))

        block_index = d.pop("block_index")

        def _parse_block(
            data: object,
        ) -> Union[
            "ModelOutputTextStreamBlock",
            "ModelOutputThinkingStreamBlock",
            "ModelOutputToolUseStreamBlock",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_model_output_stream_block_type_0 = (
                    ModelOutputTextStreamBlock.from_dict(data)
                )

                return componentsschemas_model_output_stream_block_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_model_output_stream_block_type_1 = (
                    ModelOutputThinkingStreamBlock.from_dict(data)
                )

                return componentsschemas_model_output_stream_block_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_model_output_stream_block_type_2 = (
                ModelOutputToolUseStreamBlock.from_dict(data)
            )

            return componentsschemas_model_output_stream_block_type_2

        block = _parse_block(d.pop("block"))

        model_output_block_start_delta = cls(
            kind=kind,
            block_index=block_index,
            block=block,
        )

        return model_output_block_start_delta
