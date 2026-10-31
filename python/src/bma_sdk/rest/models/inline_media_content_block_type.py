from typing import Literal, cast

InlineMediaContentBlockType = Literal["media"]

INLINE_MEDIA_CONTENT_BLOCK_TYPE_VALUES: set[InlineMediaContentBlockType] = {
    "media",
}


def check_inline_media_content_block_type(value: str) -> InlineMediaContentBlockType:
    if value in INLINE_MEDIA_CONTENT_BLOCK_TYPE_VALUES:
        return cast(InlineMediaContentBlockType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {INLINE_MEDIA_CONTENT_BLOCK_TYPE_VALUES!r}"
    )
