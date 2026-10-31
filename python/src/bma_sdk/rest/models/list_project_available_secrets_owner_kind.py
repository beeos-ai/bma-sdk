from typing import Literal, cast

ListProjectAvailableSecretsOwnerKind = Literal["org", "project", "user"]

LIST_PROJECT_AVAILABLE_SECRETS_OWNER_KIND_VALUES: set[
    ListProjectAvailableSecretsOwnerKind
] = {
    "org",
    "project",
    "user",
}


def check_list_project_available_secrets_owner_kind(
    value: str,
) -> ListProjectAvailableSecretsOwnerKind:
    if value in LIST_PROJECT_AVAILABLE_SECRETS_OWNER_KIND_VALUES:
        return cast(ListProjectAvailableSecretsOwnerKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_PROJECT_AVAILABLE_SECRETS_OWNER_KIND_VALUES!r}"
    )
