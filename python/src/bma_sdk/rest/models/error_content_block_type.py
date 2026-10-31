from typing import Literal, cast

ErrorContentBlockType = Literal["error"]

ERROR_CONTENT_BLOCK_TYPE_VALUES: set[ErrorContentBlockType] = {
    "error",
}


def check_error_content_block_type(value: str) -> ErrorContentBlockType:
    if value in ERROR_CONTENT_BLOCK_TYPE_VALUES:
        return cast(ErrorContentBlockType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ERROR_CONTENT_BLOCK_TYPE_VALUES!r}"
    )
