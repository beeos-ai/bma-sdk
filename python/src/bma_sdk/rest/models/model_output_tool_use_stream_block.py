from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.model_output_tool_use_stream_block_kind import (
    ModelOutputToolUseStreamBlockKind,
    check_model_output_tool_use_stream_block_kind,
)

T = TypeVar("T", bound="ModelOutputToolUseStreamBlock")


@_attrs_define
class ModelOutputToolUseStreamBlock:
    """
    Attributes:
        kind (ModelOutputToolUseStreamBlockKind):
        tool_call_id (str):
        tool_name (str):
    """

    kind: ModelOutputToolUseStreamBlockKind
    tool_call_id: str
    tool_name: str

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        tool_call_id = self.tool_call_id

        tool_name = self.tool_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "tool_call_id": tool_call_id,
                "tool_name": tool_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_model_output_tool_use_stream_block_kind(d.pop("kind"))

        tool_call_id = d.pop("tool_call_id")

        tool_name = d.pop("tool_name")

        model_output_tool_use_stream_block = cls(
            kind=kind,
            tool_call_id=tool_call_id,
            tool_name=tool_name,
        )

        return model_output_tool_use_stream_block
