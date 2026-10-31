from typing import Literal, cast

SubmitToolCallResultRequestOutcome = Literal["failed", "succeeded"]

SUBMIT_TOOL_CALL_RESULT_REQUEST_OUTCOME_VALUES: set[
    SubmitToolCallResultRequestOutcome
] = {
    "failed",
    "succeeded",
}


def check_submit_tool_call_result_request_outcome(
    value: str,
) -> SubmitToolCallResultRequestOutcome:
    if value in SUBMIT_TOOL_CALL_RESULT_REQUEST_OUTCOME_VALUES:
        return cast(SubmitToolCallResultRequestOutcome, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {SUBMIT_TOOL_CALL_RESULT_REQUEST_OUTCOME_VALUES!r}"
    )
