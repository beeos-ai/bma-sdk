from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="MachineInteractionPermissions")


@_attrs_define
class MachineInteractionPermissions:
    """
    Attributes:
        terminal (bool):
        desktop_watch (bool):
        desktop_control (bool):
    """

    terminal: bool
    desktop_watch: bool
    desktop_control: bool

    def to_dict(self) -> dict[str, Any]:
        terminal = self.terminal

        desktop_watch = self.desktop_watch

        desktop_control = self.desktop_control

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "terminal": terminal,
                "desktop_watch": desktop_watch,
                "desktop_control": desktop_control,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        terminal = d.pop("terminal")

        desktop_watch = d.pop("desktop_watch")

        desktop_control = d.pop("desktop_control")

        machine_interaction_permissions = cls(
            terminal=terminal,
            desktop_watch=desktop_watch,
            desktop_control=desktop_control,
        )

        return machine_interaction_permissions
