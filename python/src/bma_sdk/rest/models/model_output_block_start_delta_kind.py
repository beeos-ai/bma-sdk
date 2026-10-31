from typing import Literal, cast

ModelOutputBlockStartDeltaKind = Literal["block_start"]

MODEL_OUTPUT_BLOCK_START_DELTA_KIND_VALUES: set[ModelOutputBlockStartDeltaKind] = {
    "block_start",
}


def check_model_output_block_start_delta_kind(
    value: str,
) -> ModelOutputBlockStartDeltaKind:
    if value in MODEL_OUTPUT_BLOCK_START_DELTA_KIND_VALUES:
        return cast(ModelOutputBlockStartDeltaKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_OUTPUT_BLOCK_START_DELTA_KIND_VALUES!r}"
    )
