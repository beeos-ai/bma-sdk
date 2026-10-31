from typing import Literal, cast

ResourceListSort = Literal[
    "-created_at", "-name", "-updated_at", "created_at", "name", "updated_at"
]

RESOURCE_LIST_SORT_VALUES: set[ResourceListSort] = {
    "-created_at",
    "-name",
    "-updated_at",
    "created_at",
    "name",
    "updated_at",
}


def check_resource_list_sort(value: str) -> ResourceListSort:
    if value in RESOURCE_LIST_SORT_VALUES:
        return cast(ResourceListSort, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {RESOURCE_LIST_SORT_VALUES!r}"
    )
