from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UpdateSkillRequestType1")


@_attrs_define
class UpdateSkillRequestType1:
    """
    Attributes:
        skill_md (str):
    """

    skill_md: str

    def to_dict(self) -> dict[str, Any]:
        skill_md = self.skill_md

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "skill_md": skill_md,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        skill_md = d.pop("skill_md")

        update_skill_request_type_1 = cls(
            skill_md=skill_md,
        )

        return update_skill_request_type_1
