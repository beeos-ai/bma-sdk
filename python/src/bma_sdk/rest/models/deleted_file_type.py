from typing import Literal, cast

DeletedFileType = Literal["file_deleted"]

DELETED_FILE_TYPE_VALUES: set[DeletedFileType] = {
    "file_deleted",
}


def check_deleted_file_type(value: str) -> DeletedFileType:
    if value in DELETED_FILE_TYPE_VALUES:
        return cast(DeletedFileType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {DELETED_FILE_TYPE_VALUES!r}"
    )
