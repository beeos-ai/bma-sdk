from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.model_tool_call_content_block_type import (
    ModelToolCallContentBlockType,
    check_model_tool_call_content_block_type,
)
from ..models.tool_call_type import ToolCallType, check_tool_call_type
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.content_block_metadata import ContentBlockMetadata
    from ..models.tool_input import ToolInput


T = TypeVar("T", bound="ModelToolCallContentBlock")


@_attrs_define
class ModelToolCallContentBlock:
    """
    Attributes:
        type_ (ModelToolCallContentBlockType):
        tool_call_id (str):
        tool_type (ToolCallType): Identifies who manages execution. Built-in and MCP calls are platform-managed; custom
            calls wait for an external consumer to submit their result.
        name (str):
        input_ (ToolInput): Non-null JSON object containing the arguments emitted for a tool call.
        metadata (Union[Unset, ContentBlockMetadata]): Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64
            characters, values must be strings of up to 512 characters.
    """

    type_: ModelToolCallContentBlockType
    tool_call_id: str
    tool_type: ToolCallType
    name: str
    input_: "ToolInput"
    metadata: Union[Unset, "ContentBlockMetadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        tool_call_id = self.tool_call_id

        tool_type: str = self.tool_type

        name = self.name

        input_ = self.input_.to_dict()

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "tool_call_id": tool_call_id,
                "tool_type": tool_type,
                "name": name,
                "input": input_,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.content_block_metadata import ContentBlockMetadata
        from ..models.tool_input import ToolInput

        d = dict(src_dict)
        type_ = check_model_tool_call_content_block_type(d.pop("type"))

        tool_call_id = d.pop("tool_call_id")

        tool_type = check_tool_call_type(d.pop("tool_type"))

        name = d.pop("name")

        input_ = ToolInput.from_dict(d.pop("input"))

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, ContentBlockMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ContentBlockMetadata.from_dict(_metadata)

        model_tool_call_content_block = cls(
            type_=type_,
            tool_call_id=tool_call_id,
            tool_type=tool_type,
            name=name,
            input_=input_,
            metadata=metadata,
        )

        return model_tool_call_content_block
