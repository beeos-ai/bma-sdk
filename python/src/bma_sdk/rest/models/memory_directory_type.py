from typing import Literal, cast

MemoryDirectoryType = Literal["directory"]

MEMORY_DIRECTORY_TYPE_VALUES: set[MemoryDirectoryType] = {
    "directory",
}


def check_memory_directory_type(value: str) -> MemoryDirectoryType:
    if value in MEMORY_DIRECTORY_TYPE_VALUES:
        return cast(MemoryDirectoryType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MEMORY_DIRECTORY_TYPE_VALUES!r}"
    )
