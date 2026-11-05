from typing import Literal, cast

CompiledHarnessKind = Literal["acp"]

COMPILED_HARNESS_KIND_VALUES: set[CompiledHarnessKind] = {
    "acp",
}


def check_compiled_harness_kind(value: str) -> CompiledHarnessKind:
    if value in COMPILED_HARNESS_KIND_VALUES:
        return cast(CompiledHarnessKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {COMPILED_HARNESS_KIND_VALUES!r}"
    )
