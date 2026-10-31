from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.desktop_action_kind import DesktopActionKind, check_desktop_action_kind
from ..types import UNSET, Unset

T = TypeVar("T", bound="DesktopAction")


@_attrs_define
class DesktopAction:
    """
    Attributes:
        kind (DesktopActionKind):
        x (Union[Unset, int]):
        y (Union[Unset, int]):
        button (Union[Unset, int]):
        pressed (Union[Unset, bool]):
        keysym (Union[Unset, int]):
        text (Union[Unset, str]):
        delta_x (Union[Unset, int]):
        delta_y (Union[Unset, int]):
    """

    kind: DesktopActionKind
    x: Union[Unset, int] = UNSET
    y: Union[Unset, int] = UNSET
    button: Union[Unset, int] = UNSET
    pressed: Union[Unset, bool] = UNSET
    keysym: Union[Unset, int] = UNSET
    text: Union[Unset, str] = UNSET
    delta_x: Union[Unset, int] = UNSET
    delta_y: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        x = self.x

        y = self.y

        button = self.button

        pressed = self.pressed

        keysym = self.keysym

        text = self.text

        delta_x = self.delta_x

        delta_y = self.delta_y

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
            }
        )
        if x is not UNSET:
            field_dict["x"] = x
        if y is not UNSET:
            field_dict["y"] = y
        if button is not UNSET:
            field_dict["button"] = button
        if pressed is not UNSET:
            field_dict["pressed"] = pressed
        if keysym is not UNSET:
            field_dict["keysym"] = keysym
        if text is not UNSET:
            field_dict["text"] = text
        if delta_x is not UNSET:
            field_dict["delta_x"] = delta_x
        if delta_y is not UNSET:
            field_dict["delta_y"] = delta_y

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_desktop_action_kind(d.pop("kind"))

        x = d.pop("x", UNSET)

        y = d.pop("y", UNSET)

        button = d.pop("button", UNSET)

        pressed = d.pop("pressed", UNSET)

        keysym = d.pop("keysym", UNSET)

        text = d.pop("text", UNSET)

        delta_x = d.pop("delta_x", UNSET)

        delta_y = d.pop("delta_y", UNSET)

        desktop_action = cls(
            kind=kind,
            x=x,
            y=y,
            button=button,
            pressed=pressed,
            keysym=keysym,
            text=text,
            delta_x=delta_x,
            delta_y=delta_y,
        )

        return desktop_action
