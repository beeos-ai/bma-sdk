from typing import Literal, cast

ProjectSecretOwnerKind = Literal["project"]

PROJECT_SECRET_OWNER_KIND_VALUES: set[ProjectSecretOwnerKind] = {
    "project",
}


def check_project_secret_owner_kind(value: str) -> ProjectSecretOwnerKind:
    if value in PROJECT_SECRET_OWNER_KIND_VALUES:
        return cast(ProjectSecretOwnerKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROJECT_SECRET_OWNER_KIND_VALUES!r}"
    )
