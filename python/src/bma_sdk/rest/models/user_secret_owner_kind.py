from typing import Literal, cast

UserSecretOwnerKind = Literal["user"]

USER_SECRET_OWNER_KIND_VALUES: set[UserSecretOwnerKind] = {
    "user",
}


def check_user_secret_owner_kind(value: str) -> UserSecretOwnerKind:
    if value in USER_SECRET_OWNER_KIND_VALUES:
        return cast(UserSecretOwnerKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {USER_SECRET_OWNER_KIND_VALUES!r}"
    )
