from typing import Literal, cast

DeletedSessionResourceType = Literal["session_resource_deleted"]

DELETED_SESSION_RESOURCE_TYPE_VALUES: set[DeletedSessionResourceType] = {
    "session_resource_deleted",
}


def check_deleted_session_resource_type(value: str) -> DeletedSessionResourceType:
    if value in DELETED_SESSION_RESOURCE_TYPE_VALUES:
        return cast(DeletedSessionResourceType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {DELETED_SESSION_RESOURCE_TYPE_VALUES!r}"
    )
