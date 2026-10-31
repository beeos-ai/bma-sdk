from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.direct_skill_availability import DirectSkillAvailability
    from ..models.granted_skill_availability import GrantedSkillAvailability
    from ..models.skill import Skill


T = TypeVar("T", bound="ProjectSkillAccess")


@_attrs_define
class ProjectSkillAccess:
    """
    Attributes:
        skill (Skill):
        project_id (str): Project ID (proj_...).
        availability (Union['DirectSkillAvailability', 'GrantedSkillAvailability']):
    """

    skill: "Skill"
    project_id: str
    availability: Union["DirectSkillAvailability", "GrantedSkillAvailability"]

    def to_dict(self) -> dict[str, Any]:
        from ..models.direct_skill_availability import DirectSkillAvailability

        skill = self.skill.to_dict()

        project_id = self.project_id

        availability: dict[str, Any]
        if isinstance(self.availability, DirectSkillAvailability):
            availability = self.availability.to_dict()
        else:
            availability = self.availability.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "skill": skill,
                "project_id": project_id,
                "availability": availability,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.direct_skill_availability import DirectSkillAvailability
        from ..models.granted_skill_availability import GrantedSkillAvailability
        from ..models.skill import Skill

        d = dict(src_dict)
        skill = Skill.from_dict(d.pop("skill"))

        project_id = d.pop("project_id")

        def _parse_availability(
            data: object,
        ) -> Union["DirectSkillAvailability", "GrantedSkillAvailability"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_skill_availability_type_0 = (
                    DirectSkillAvailability.from_dict(data)
                )

                return componentsschemas_skill_availability_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_skill_availability_type_1 = (
                GrantedSkillAvailability.from_dict(data)
            )

            return componentsschemas_skill_availability_type_1

        availability = _parse_availability(d.pop("availability"))

        project_skill_access = cls(
            skill=skill,
            project_id=project_id,
            availability=availability,
        )

        return project_skill_access
