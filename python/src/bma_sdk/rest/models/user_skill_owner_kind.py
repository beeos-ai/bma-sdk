from typing import Literal, cast

UserSkillOwnerKind = Literal["user"]

USER_SKILL_OWNER_KIND_VALUES: set[UserSkillOwnerKind] = {
    "user",
}


def check_user_skill_owner_kind(value: str) -> UserSkillOwnerKind:
    if value in USER_SKILL_OWNER_KIND_VALUES:
        return cast(UserSkillOwnerKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {USER_SKILL_OWNER_KIND_VALUES!r}"
    )
