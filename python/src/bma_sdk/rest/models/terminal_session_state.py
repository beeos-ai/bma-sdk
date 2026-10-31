from typing import Literal, cast

TerminalSessionState = Literal["closed", "closing", "failed", "running", "starting"]

TERMINAL_SESSION_STATE_VALUES: set[TerminalSessionState] = {
    "closed",
    "closing",
    "failed",
    "running",
    "starting",
}


def check_terminal_session_state(value: str) -> TerminalSessionState:
    if value in TERMINAL_SESSION_STATE_VALUES:
        return cast(TerminalSessionState, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {TERMINAL_SESSION_STATE_VALUES!r}"
    )
