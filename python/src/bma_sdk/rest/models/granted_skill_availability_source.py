from typing import Literal, cast

GrantedSkillAvailabilitySource = Literal["grant"]

GRANTED_SKILL_AVAILABILITY_SOURCE_VALUES: set[GrantedSkillAvailabilitySource] = {
    "grant",
}


def check_granted_skill_availability_source(
    value: str,
) -> GrantedSkillAvailabilitySource:
    if value in GRANTED_SKILL_AVAILABILITY_SOURCE_VALUES:
        return cast(GrantedSkillAvailabilitySource, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GRANTED_SKILL_AVAILABILITY_SOURCE_VALUES!r}"
    )
