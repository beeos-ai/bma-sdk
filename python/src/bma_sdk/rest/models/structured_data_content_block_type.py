from typing import Literal, cast

StructuredDataContentBlockType = Literal["structured_data"]

STRUCTURED_DATA_CONTENT_BLOCK_TYPE_VALUES: set[StructuredDataContentBlockType] = {
    "structured_data",
}


def check_structured_data_content_block_type(
    value: str,
) -> StructuredDataContentBlockType:
    if value in STRUCTURED_DATA_CONTENT_BLOCK_TYPE_VALUES:
        return cast(StructuredDataContentBlockType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {STRUCTURED_DATA_CONTENT_BLOCK_TYPE_VALUES!r}"
    )
