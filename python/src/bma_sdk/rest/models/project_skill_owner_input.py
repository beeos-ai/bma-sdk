from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.project_skill_owner_input_kind import (
    ProjectSkillOwnerInputKind,
    check_project_skill_owner_input_kind,
)

T = TypeVar("T", bound="ProjectSkillOwnerInput")


@_attrs_define
class ProjectSkillOwnerInput:
    """
    Attributes:
        kind (ProjectSkillOwnerInputKind):
        project_id (str): Project ID (proj_...).
    """

    kind: ProjectSkillOwnerInputKind
    project_id: str

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        project_id = self.project_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "project_id": project_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_project_skill_owner_input_kind(d.pop("kind"))

        project_id = d.pop("project_id")

        project_skill_owner_input = cls(
            kind=kind,
            project_id=project_id,
        )

        return project_skill_owner_input
