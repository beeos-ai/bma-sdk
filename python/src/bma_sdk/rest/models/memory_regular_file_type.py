from typing import Literal, cast

MemoryRegularFileType = Literal["file"]

MEMORY_REGULAR_FILE_TYPE_VALUES: set[MemoryRegularFileType] = {
    "file",
}


def check_memory_regular_file_type(value: str) -> MemoryRegularFileType:
    if value in MEMORY_REGULAR_FILE_TYPE_VALUES:
        return cast(MemoryRegularFileType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MEMORY_REGULAR_FILE_TYPE_VALUES!r}"
    )
