from typing import Literal, cast

SessionFileResourceType = Literal["file"]

SESSION_FILE_RESOURCE_TYPE_VALUES: set[SessionFileResourceType] = {
    "file",
}


def check_session_file_resource_type(value: str) -> SessionFileResourceType:
    if value in SESSION_FILE_RESOURCE_TYPE_VALUES:
        return cast(SessionFileResourceType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {SESSION_FILE_RESOURCE_TYPE_VALUES!r}"
    )
