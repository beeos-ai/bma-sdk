from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config_error_issue import AgentConfigErrorIssue


T = TypeVar("T", bound="Error")


@_attrs_define
class Error:
    """
    Attributes:
        error (str): Human-readable error message. Do not match on it programmatically.
        code (str): Stable error code for programmatic handling.
        current_digest (Union[Unset, str]): Current file digest for file_content_conflict or expected_digest_required;
            absent if the file no longer exists. A replacement must be confirmed before retrying with this digest.
        issues (Union[Unset, list['AgentConfigErrorIssue']]): Field-level problems when a submitted document (such as an
            agent config source) failed validation. Absent for errors that are not about a specific field.
    """

    error: str
    code: str
    current_digest: Union[Unset, str] = UNSET
    issues: Union[Unset, list["AgentConfigErrorIssue"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        error = self.error

        code = self.code

        current_digest = self.current_digest

        issues: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.issues, Unset):
            issues = []
            for issues_item_data in self.issues:
                issues_item = issues_item_data.to_dict()
                issues.append(issues_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "error": error,
                "code": code,
            }
        )
        if current_digest is not UNSET:
            field_dict["current_digest"] = current_digest
        if issues is not UNSET:
            field_dict["issues"] = issues

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_error_issue import AgentConfigErrorIssue

        d = dict(src_dict)
        error = d.pop("error")

        code = d.pop("code")

        current_digest = d.pop("current_digest", UNSET)

        issues = []
        _issues = d.pop("issues", UNSET)
        for issues_item_data in _issues or []:
            issues_item = AgentConfigErrorIssue.from_dict(issues_item_data)

            issues.append(issues_item)

        error = cls(
            error=error,
            code=code,
            current_digest=current_digest,
            issues=issues,
        )

        return error
