from typing import Literal, cast

ProjectSecretOwnerInputKind = Literal["project"]

PROJECT_SECRET_OWNER_INPUT_KIND_VALUES: set[ProjectSecretOwnerInputKind] = {
    "project",
}


def check_project_secret_owner_input_kind(value: str) -> ProjectSecretOwnerInputKind:
    if value in PROJECT_SECRET_OWNER_INPUT_KIND_VALUES:
        return cast(ProjectSecretOwnerInputKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROJECT_SECRET_OWNER_INPUT_KIND_VALUES!r}"
    )
