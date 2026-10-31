from typing import Literal, cast

ListProjectAvailableSkillsOwnerKind = Literal["org", "project", "user"]

LIST_PROJECT_AVAILABLE_SKILLS_OWNER_KIND_VALUES: set[
    ListProjectAvailableSkillsOwnerKind
] = {
    "org",
    "project",
    "user",
}


def check_list_project_available_skills_owner_kind(
    value: str,
) -> ListProjectAvailableSkillsOwnerKind:
    if value in LIST_PROJECT_AVAILABLE_SKILLS_OWNER_KIND_VALUES:
        return cast(ListProjectAvailableSkillsOwnerKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_PROJECT_AVAILABLE_SKILLS_OWNER_KIND_VALUES!r}"
    )
