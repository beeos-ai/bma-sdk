from typing import Literal, cast

MachineSourceKind = Literal["byo", "pool"]

MACHINE_SOURCE_KIND_VALUES: set[MachineSourceKind] = {
    "byo",
    "pool",
}


def check_machine_source_kind(value: str) -> MachineSourceKind:
    if value in MACHINE_SOURCE_KIND_VALUES:
        return cast(MachineSourceKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MACHINE_SOURCE_KIND_VALUES!r}"
    )
