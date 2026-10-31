from typing import Literal, cast

ArtifactOrigin = Literal["input", "machine_upload", "tool_output"]

ARTIFACT_ORIGIN_VALUES: set[ArtifactOrigin] = {
    "input",
    "machine_upload",
    "tool_output",
}


def check_artifact_origin(value: str) -> ArtifactOrigin:
    if value in ARTIFACT_ORIGIN_VALUES:
        return cast(ArtifactOrigin, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ARTIFACT_ORIGIN_VALUES!r}"
    )
