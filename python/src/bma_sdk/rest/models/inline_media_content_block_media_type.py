from typing import Literal, cast

InlineMediaContentBlockMediaType = Literal[
    "application/msword",
    "application/pdf",
    "application/rtf",
    "application/vnd.apple.iwork",
    "application/vnd.apple.keynote",
    "application/vnd.apple.pages",
    "application/vnd.ms-excel",
    "application/vnd.ms-powerpoint",
    "application/vnd.oasis.opendocument.text",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "image/gif",
    "image/jpeg",
    "image/png",
    "image/webp",
    "text/csv",
    "text/markdown",
    "text/plain",
    "text/tab-separated-values",
    "text/x-iif",
]

INLINE_MEDIA_CONTENT_BLOCK_MEDIA_TYPE_VALUES: set[InlineMediaContentBlockMediaType] = {
    "application/msword",
    "application/pdf",
    "application/rtf",
    "application/vnd.apple.iwork",
    "application/vnd.apple.keynote",
    "application/vnd.apple.pages",
    "application/vnd.ms-excel",
    "application/vnd.ms-powerpoint",
    "application/vnd.oasis.opendocument.text",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "image/gif",
    "image/jpeg",
    "image/png",
    "image/webp",
    "text/csv",
    "text/markdown",
    "text/plain",
    "text/tab-separated-values",
    "text/x-iif",
}


def check_inline_media_content_block_media_type(
    value: str,
) -> InlineMediaContentBlockMediaType:
    if value in INLINE_MEDIA_CONTENT_BLOCK_MEDIA_TYPE_VALUES:
        return cast(InlineMediaContentBlockMediaType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {INLINE_MEDIA_CONTENT_BLOCK_MEDIA_TYPE_VALUES!r}"
    )
