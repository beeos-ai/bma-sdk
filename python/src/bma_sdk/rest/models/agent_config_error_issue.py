from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentConfigErrorIssue")


@_attrs_define
class AgentConfigErrorIssue:
    """
    Attributes:
        path (str): JSON Pointer (RFC 6901) to the offending field in the submitted document. An empty string refers to
            the whole document.
        message (str): Human-readable description of the problem with this field.
        line (Union[Unset, int]): 1-based line of the offending field in the submitted source, when it can be located.
        column (Union[Unset, int]): 1-based column of the offending field in the submitted source, when it can be
            located.
    """

    path: str
    message: str
    line: Union[Unset, int] = UNSET
    column: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        path = self.path

        message = self.message

        line = self.line

        column = self.column

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "path": path,
                "message": message,
            }
        )
        if line is not UNSET:
            field_dict["line"] = line
        if column is not UNSET:
            field_dict["column"] = column

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        path = d.pop("path")

        message = d.pop("message")

        line = d.pop("line", UNSET)

        column = d.pop("column", UNSET)

        agent_config_error_issue = cls(
            path=path,
            message=message,
            line=line,
            column=column,
        )

        return agent_config_error_issue
