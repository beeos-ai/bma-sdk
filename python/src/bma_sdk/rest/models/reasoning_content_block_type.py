from typing import Literal, cast

ReasoningContentBlockType = Literal["reasoning"]

REASONING_CONTENT_BLOCK_TYPE_VALUES: set[ReasoningContentBlockType] = {
    "reasoning",
}


def check_reasoning_content_block_type(value: str) -> ReasoningContentBlockType:
    if value in REASONING_CONTENT_BLOCK_TYPE_VALUES:
        return cast(ReasoningContentBlockType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {REASONING_CONTENT_BLOCK_TYPE_VALUES!r}"
    )
