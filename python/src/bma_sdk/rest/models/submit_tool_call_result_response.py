from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.tool_call import ToolCall
    from ..models.tool_result import ToolResult


T = TypeVar("T", bound="SubmitToolCallResultResponse")


@_attrs_define
class SubmitToolCallResultResponse:
    """
    Attributes:
        tool_call (ToolCall): A model-emitted tool call together with its current lifecycle state.
        tool_result (ToolResult):
    """

    tool_call: "ToolCall"
    tool_result: "ToolResult"

    def to_dict(self) -> dict[str, Any]:
        tool_call = self.tool_call.to_dict()

        tool_result = self.tool_result.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "tool_call": tool_call,
                "tool_result": tool_result,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tool_call import ToolCall
        from ..models.tool_result import ToolResult

        d = dict(src_dict)
        tool_call = ToolCall.from_dict(d.pop("tool_call"))

        tool_result = ToolResult.from_dict(d.pop("tool_result"))

        submit_tool_call_result_response = cls(
            tool_call=tool_call,
            tool_result=tool_result,
        )

        return submit_tool_call_result_response
