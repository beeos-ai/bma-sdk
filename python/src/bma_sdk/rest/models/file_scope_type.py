from typing import Literal, cast

FileScopeType = Literal["session"]

FILE_SCOPE_TYPE_VALUES: set[FileScopeType] = {
    "session",
}


def check_file_scope_type(value: str) -> FileScopeType:
    if value in FILE_SCOPE_TYPE_VALUES:
        return cast(FileScopeType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {FILE_SCOPE_TYPE_VALUES!r}"
    )
