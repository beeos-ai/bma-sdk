from typing import Literal, cast

ModelOutputBlockStopDeltaKind = Literal["block_stop"]

MODEL_OUTPUT_BLOCK_STOP_DELTA_KIND_VALUES: set[ModelOutputBlockStopDeltaKind] = {
    "block_stop",
}


def check_model_output_block_stop_delta_kind(
    value: str,
) -> ModelOutputBlockStopDeltaKind:
    if value in MODEL_OUTPUT_BLOCK_STOP_DELTA_KIND_VALUES:
        return cast(ModelOutputBlockStopDeltaKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MODEL_OUTPUT_BLOCK_STOP_DELTA_KIND_VALUES!r}"
    )
