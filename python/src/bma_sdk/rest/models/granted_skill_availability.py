from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.granted_skill_availability_source import (
    GrantedSkillAvailabilitySource,
    check_granted_skill_availability_source,
)

T = TypeVar("T", bound="GrantedSkillAvailability")


@_attrs_define
class GrantedSkillAvailability:
    """
    Attributes:
        source (GrantedSkillAvailabilitySource):
        grant_id (str):
    """

    source: GrantedSkillAvailabilitySource
    grant_id: str

    def to_dict(self) -> dict[str, Any]:
        source: str = self.source

        grant_id = self.grant_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "source": source,
                "grant_id": grant_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = check_granted_skill_availability_source(d.pop("source"))

        grant_id = d.pop("grant_id")

        granted_skill_availability = cls(
            source=source,
            grant_id=grant_id,
        )

        return granted_skill_availability
