from typing import Literal, cast

DesktopActionKind = Literal["key", "pointer_button", "pointer_move", "text", "wheel"]

DESKTOP_ACTION_KIND_VALUES: set[DesktopActionKind] = {
    "key",
    "pointer_button",
    "pointer_move",
    "text",
    "wheel",
}


def check_desktop_action_kind(value: str) -> DesktopActionKind:
    if value in DESKTOP_ACTION_KIND_VALUES:
        return cast(DesktopActionKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {DESKTOP_ACTION_KIND_VALUES!r}"
    )
