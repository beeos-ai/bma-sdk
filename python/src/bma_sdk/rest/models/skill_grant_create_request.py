from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="SkillGrantCreateRequest")


@_attrs_define
class SkillGrantCreateRequest:
    """
    Attributes:
        target_project_id (str): Project ID (proj_...).
    """

    target_project_id: str

    def to_dict(self) -> dict[str, Any]:
        target_project_id = self.target_project_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "target_project_id": target_project_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        target_project_id = d.pop("target_project_id")

        skill_grant_create_request = cls(
            target_project_id=target_project_id,
        )

        return skill_grant_create_request
