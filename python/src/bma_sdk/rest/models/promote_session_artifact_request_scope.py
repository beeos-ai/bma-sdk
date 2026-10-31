from typing import Literal, cast

PromoteSessionArtifactRequestScope = Literal["project", "session"]

PROMOTE_SESSION_ARTIFACT_REQUEST_SCOPE_VALUES: set[
    PromoteSessionArtifactRequestScope
] = {
    "project",
    "session",
}


def check_promote_session_artifact_request_scope(
    value: str,
) -> PromoteSessionArtifactRequestScope:
    if value in PROMOTE_SESSION_ARTIFACT_REQUEST_SCOPE_VALUES:
        return cast(PromoteSessionArtifactRequestScope, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {PROMOTE_SESSION_ARTIFACT_REQUEST_SCOPE_VALUES!r}"
    )
