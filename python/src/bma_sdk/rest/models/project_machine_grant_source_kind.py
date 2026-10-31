from typing import Literal, cast

ProjectMachineGrantSourceKind = Literal["explicit", "pool"]

PROJECT_MACHINE_GRANT_SOURCE_KIND_VALUES: set[ProjectMachineGrantSourceKind] = {
    "explicit",
    "pool",
}


def check_project_machine_grant_source_kind(
    value: str,
) -> ProjectMachineGrantSourceKind:
    if value in PROJECT_MACHINE_GRANT_SOURCE_KIND_VALUES:
        return cast(ProjectMachineGrantSourceKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROJECT_MACHINE_GRANT_SOURCE_KIND_VALUES!r}"
    )
