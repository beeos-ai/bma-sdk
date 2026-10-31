from typing import Literal, cast

MachineAccessSourceKind = Literal["org_role", "project_machine_grant"]

MACHINE_ACCESS_SOURCE_KIND_VALUES: set[MachineAccessSourceKind] = {
    "org_role",
    "project_machine_grant",
}


def check_machine_access_source_kind(value: str) -> MachineAccessSourceKind:
    if value in MACHINE_ACCESS_SOURCE_KIND_VALUES:
        return cast(MachineAccessSourceKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MACHINE_ACCESS_SOURCE_KIND_VALUES!r}"
    )
