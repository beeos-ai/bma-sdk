from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.direct_skill_availability_source import (
    DirectSkillAvailabilitySource,
    check_direct_skill_availability_source,
)

T = TypeVar("T", bound="DirectSkillAvailability")


@_attrs_define
class DirectSkillAvailability:
    """
    Attributes:
        source (DirectSkillAvailabilitySource):
    """

    source: DirectSkillAvailabilitySource

    def to_dict(self) -> dict[str, Any]:
        source: str = self.source

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "source": source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = check_direct_skill_availability_source(d.pop("source"))

        direct_skill_availability = cls(
            source=source,
        )

        return direct_skill_availability
