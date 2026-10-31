from typing import Literal, cast

FileResourceType = Literal["file"]

FILE_RESOURCE_TYPE_VALUES: set[FileResourceType] = {
    "file",
}


def check_file_resource_type(value: str) -> FileResourceType:
    if value in FILE_RESOURCE_TYPE_VALUES:
        return cast(FileResourceType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {FILE_RESOURCE_TYPE_VALUES!r}"
    )
