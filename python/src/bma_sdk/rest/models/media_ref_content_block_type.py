from typing import Literal, cast

MediaRefContentBlockType = Literal["media_ref"]

MEDIA_REF_CONTENT_BLOCK_TYPE_VALUES: set[MediaRefContentBlockType] = {
    "media_ref",
}


def check_media_ref_content_block_type(value: str) -> MediaRefContentBlockType:
    if value in MEDIA_REF_CONTENT_BLOCK_TYPE_VALUES:
        return cast(MediaRefContentBlockType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MEDIA_REF_CONTENT_BLOCK_TYPE_VALUES!r}"
    )
