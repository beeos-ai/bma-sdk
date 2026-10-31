from typing import Literal, cast

ProjectFileType = Literal["file"]

PROJECT_FILE_TYPE_VALUES: set[ProjectFileType] = {
    "file",
}


def check_project_file_type(value: str) -> ProjectFileType:
    if value in PROJECT_FILE_TYPE_VALUES:
        return cast(ProjectFileType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROJECT_FILE_TYPE_VALUES!r}"
    )
