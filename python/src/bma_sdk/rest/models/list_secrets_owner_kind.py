from typing import Literal, cast

ListSecretsOwnerKind = Literal["org", "project", "user"]

LIST_SECRETS_OWNER_KIND_VALUES: set[ListSecretsOwnerKind] = {
    "org",
    "project",
    "user",
}


def check_list_secrets_owner_kind(value: str) -> ListSecretsOwnerKind:
    if value in LIST_SECRETS_OWNER_KIND_VALUES:
        return cast(ListSecretsOwnerKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_SECRETS_OWNER_KIND_VALUES!r}"
    )
