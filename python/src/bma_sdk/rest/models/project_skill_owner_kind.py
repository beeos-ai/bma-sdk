from typing import Literal, cast

ProjectSkillOwnerKind = Literal["project"]

PROJECT_SKILL_OWNER_KIND_VALUES: set[ProjectSkillOwnerKind] = {
    "project",
}


def check_project_skill_owner_kind(value: str) -> ProjectSkillOwnerKind:
    if value in PROJECT_SKILL_OWNER_KIND_VALUES:
        return cast(ProjectSkillOwnerKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROJECT_SKILL_OWNER_KIND_VALUES!r}"
    )
