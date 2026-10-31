from typing import Literal, cast

CreatedResourceListSort = Literal["-created_at", "-name", "created_at", "name"]

CREATED_RESOURCE_LIST_SORT_VALUES: set[CreatedResourceListSort] = {
    "-created_at",
    "-name",
    "created_at",
    "name",
}


def check_created_resource_list_sort(value: str) -> CreatedResourceListSort:
    if value in CREATED_RESOURCE_LIST_SORT_VALUES:
        return cast(CreatedResourceListSort, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CREATED_RESOURCE_LIST_SORT_VALUES!r}"
    )
