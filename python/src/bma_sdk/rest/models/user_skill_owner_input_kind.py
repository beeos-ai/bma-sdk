from typing import Literal, cast

UserSkillOwnerInputKind = Literal["user"]

USER_SKILL_OWNER_INPUT_KIND_VALUES: set[UserSkillOwnerInputKind] = {
    "user",
}


def check_user_skill_owner_input_kind(value: str) -> UserSkillOwnerInputKind:
    if value in USER_SKILL_OWNER_INPUT_KIND_VALUES:
        return cast(UserSkillOwnerInputKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {USER_SKILL_OWNER_INPUT_KIND_VALUES!r}"
    )
