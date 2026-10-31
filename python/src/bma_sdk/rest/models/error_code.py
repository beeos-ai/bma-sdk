from typing import Literal, cast

ErrorCode = Literal[
    "agent_backlog_full",
    "authentication_unavailable",
    "conflict",
    "csrf_check_failed",
    "daemon_runtime_unregistered",
    "expected_digest_required",
    "file_content_conflict",
    "file_read_only",
    "forbidden",
    "gone",
    "idempotency_key_conflict",
    "internal_error",
    "invalid_request",
    "managed_work_admission_denied",
    "not_a_file",
    "not_found",
    "not_wake_capable",
    "pending_work",
    "rate_limited",
    "request_too_large",
    "service_unavailable",
    "state_transition_conflict",
    "unauthorized",
    "unprocessable",
    "unsupported_media_type",
    "upstream_unavailable",
    "validation_failed",
]

ERROR_CODE_VALUES: set[ErrorCode] = {
    "agent_backlog_full",
    "authentication_unavailable",
    "conflict",
    "csrf_check_failed",
    "daemon_runtime_unregistered",
    "expected_digest_required",
    "file_content_conflict",
    "file_read_only",
    "forbidden",
    "gone",
    "idempotency_key_conflict",
    "internal_error",
    "invalid_request",
    "managed_work_admission_denied",
    "not_a_file",
    "not_found",
    "not_wake_capable",
    "pending_work",
    "rate_limited",
    "request_too_large",
    "service_unavailable",
    "state_transition_conflict",
    "unauthorized",
    "unprocessable",
    "unsupported_media_type",
    "upstream_unavailable",
    "validation_failed",
}


def check_error_code(value: str) -> ErrorCode:
    if value in ERROR_CODE_VALUES:
        return cast(ErrorCode, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ERROR_CODE_VALUES!r}"
    )
