from typing import Literal, cast

DirectSkillAvailabilitySource = Literal["direct"]

DIRECT_SKILL_AVAILABILITY_SOURCE_VALUES: set[DirectSkillAvailabilitySource] = {
    "direct",
}


def check_direct_skill_availability_source(value: str) -> DirectSkillAvailabilitySource:
    if value in DIRECT_SKILL_AVAILABILITY_SOURCE_VALUES:
        return cast(DirectSkillAvailabilitySource, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {DIRECT_SKILL_AVAILABILITY_SOURCE_VALUES!r}"
    )
