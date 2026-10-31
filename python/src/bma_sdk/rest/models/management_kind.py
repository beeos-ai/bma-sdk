from typing import Literal, cast

ManagementKind = Literal["cluster", "tenant"]

MANAGEMENT_KIND_VALUES: set[ManagementKind] = {
    "cluster",
    "tenant",
}


def check_management_kind(value: str) -> ManagementKind:
    if value in MANAGEMENT_KIND_VALUES:
        return cast(ManagementKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MANAGEMENT_KIND_VALUES!r}"
    )
