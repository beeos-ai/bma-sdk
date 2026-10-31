from typing import Literal, cast

UserSecretOwnerInputKind = Literal["user"]

USER_SECRET_OWNER_INPUT_KIND_VALUES: set[UserSecretOwnerInputKind] = {
    "user",
}


def check_user_secret_owner_input_kind(value: str) -> UserSecretOwnerInputKind:
    if value in USER_SECRET_OWNER_INPUT_KIND_VALUES:
        return cast(UserSecretOwnerInputKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {USER_SECRET_OWNER_INPUT_KIND_VALUES!r}"
    )
