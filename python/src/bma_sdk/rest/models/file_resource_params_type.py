from typing import Literal, cast

FileResourceParamsType = Literal["file"]

FILE_RESOURCE_PARAMS_TYPE_VALUES: set[FileResourceParamsType] = {
    "file",
}


def check_file_resource_params_type(value: str) -> FileResourceParamsType:
    if value in FILE_RESOURCE_PARAMS_TYPE_VALUES:
        return cast(FileResourceParamsType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {FILE_RESOURCE_PARAMS_TYPE_VALUES!r}"
    )
