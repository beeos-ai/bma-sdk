from typing import Literal, cast

TextContentBlockType = Literal["text"]

TEXT_CONTENT_BLOCK_TYPE_VALUES: set[TextContentBlockType] = {
    "text",
}


def check_text_content_block_type(value: str) -> TextContentBlockType:
    if value in TEXT_CONTENT_BLOCK_TYPE_VALUES:
        return cast(TextContentBlockType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TEXT_CONTENT_BLOCK_TYPE_VALUES!r}"
    )
