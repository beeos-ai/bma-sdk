from typing import Literal, cast

MachinePoolConnectionCheckErrorCode = Literal["unprocessable", "upstream_unavailable"]

MACHINE_POOL_CONNECTION_CHECK_ERROR_CODE_VALUES: set[
    MachinePoolConnectionCheckErrorCode
] = {
    "unprocessable",
    "upstream_unavailable",
}


def check_machine_pool_connection_check_error_code(
    value: str,
) -> MachinePoolConnectionCheckErrorCode:
    if value in MACHINE_POOL_CONNECTION_CHECK_ERROR_CODE_VALUES:
        return cast(MachinePoolConnectionCheckErrorCode, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {MACHINE_POOL_CONNECTION_CHECK_ERROR_CODE_VALUES!r}"
    )
