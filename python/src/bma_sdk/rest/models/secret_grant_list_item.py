from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.project_fields import ProjectFields
    from ..models.secret_grant import SecretGrant


T = TypeVar("T", bound="SecretGrantListItem")


@_attrs_define
class SecretGrantListItem:
    """
    Attributes:
        grant (SecretGrant):
        target_project (ProjectFields): Shared project fields composed into project response schemas. Composing schemas
            close their final shape with unevaluatedProperties.
    """

    grant: "SecretGrant"
    target_project: "ProjectFields"

    def to_dict(self) -> dict[str, Any]:
        grant = self.grant.to_dict()

        target_project = self.target_project.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "grant": grant,
                "target_project": target_project,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_fields import ProjectFields
        from ..models.secret_grant import SecretGrant

        d = dict(src_dict)
        grant = SecretGrant.from_dict(d.pop("grant"))

        target_project = ProjectFields.from_dict(d.pop("target_project"))

        secret_grant_list_item = cls(
            grant=grant,
            target_project=target_project,
        )

        return secret_grant_list_item
