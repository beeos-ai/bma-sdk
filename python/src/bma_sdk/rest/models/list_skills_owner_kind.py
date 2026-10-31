from typing import Literal, cast

ListSkillsOwnerKind = Literal["org", "project", "user"]

LIST_SKILLS_OWNER_KIND_VALUES: set[ListSkillsOwnerKind] = {
    "org",
    "project",
    "user",
}


def check_list_skills_owner_kind(value: str) -> ListSkillsOwnerKind:
    if value in LIST_SKILLS_OWNER_KIND_VALUES:
        return cast(ListSkillsOwnerKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_SKILLS_OWNER_KIND_VALUES!r}"
    )
