from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.tool_call import ToolCall


T = TypeVar("T", bound="ToolCallEnvelope")


@_attrs_define
class ToolCallEnvelope:
    """
    Attributes:
        tool_call (ToolCall): A model-emitted tool call together with its current lifecycle state.
    """

    tool_call: "ToolCall"

    def to_dict(self) -> dict[str, Any]:
        tool_call = self.tool_call.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "tool_call": tool_call,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tool_call import ToolCall

        d = dict(src_dict)
        tool_call = ToolCall.from_dict(d.pop("tool_call"))

        tool_call_envelope = cls(
            tool_call=tool_call,
        )

        return tool_call_envelope
