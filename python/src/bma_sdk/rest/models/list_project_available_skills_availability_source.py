from typing import Literal, cast

ListProjectAvailableSkillsAvailabilitySource = Literal["direct", "grant"]

LIST_PROJECT_AVAILABLE_SKILLS_AVAILABILITY_SOURCE_VALUES: set[
    ListProjectAvailableSkillsAvailabilitySource
] = {
    "direct",
    "grant",
}


def check_list_project_available_skills_availability_source(
    value: str,
) -> ListProjectAvailableSkillsAvailabilitySource:
    if value in LIST_PROJECT_AVAILABLE_SKILLS_AVAILABILITY_SOURCE_VALUES:
        return cast(ListProjectAvailableSkillsAvailabilitySource, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_PROJECT_AVAILABLE_SKILLS_AVAILABILITY_SOURCE_VALUES!r}"
    )
