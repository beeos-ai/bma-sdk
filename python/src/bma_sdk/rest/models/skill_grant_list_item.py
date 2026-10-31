from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.project_fields import ProjectFields
    from ..models.skill_grant import SkillGrant


T = TypeVar("T", bound="SkillGrantListItem")


@_attrs_define
class SkillGrantListItem:
    """
    Attributes:
        grant (SkillGrant):
        target_project (ProjectFields): Shared project fields composed into project response schemas. Composing schemas
            close their final shape with unevaluatedProperties.
    """

    grant: "SkillGrant"
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
        from ..models.skill_grant import SkillGrant

        d = dict(src_dict)
        grant = SkillGrant.from_dict(d.pop("grant"))

        target_project = ProjectFields.from_dict(d.pop("target_project"))

        skill_grant_list_item = cls(
            grant=grant,
            target_project=target_project,
        )

        return skill_grant_list_item
