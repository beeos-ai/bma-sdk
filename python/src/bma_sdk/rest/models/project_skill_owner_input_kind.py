from typing import Literal, cast

ProjectSkillOwnerInputKind = Literal["project"]

PROJECT_SKILL_OWNER_INPUT_KIND_VALUES: set[ProjectSkillOwnerInputKind] = {
    "project",
}


def check_project_skill_owner_input_kind(value: str) -> ProjectSkillOwnerInputKind:
    if value in PROJECT_SKILL_OWNER_INPUT_KIND_VALUES:
        return cast(ProjectSkillOwnerInputKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROJECT_SKILL_OWNER_INPUT_KIND_VALUES!r}"
    )
