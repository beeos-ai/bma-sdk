from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.project_event_webhook_scope_type import (
    ProjectEventWebhookScopeType,
    check_project_event_webhook_scope_type,
)

T = TypeVar("T", bound="ProjectEventWebhookScope")


@_attrs_define
class ProjectEventWebhookScope:
    """
    Attributes:
        type_ (ProjectEventWebhookScopeType):
    """

    type_: ProjectEventWebhookScopeType

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_project_event_webhook_scope_type(d.pop("type"))

        project_event_webhook_scope = cls(
            type_=type_,
        )

        return project_event_webhook_scope
