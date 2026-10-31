from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="MachineProtocolVersions")


@_attrs_define
class MachineProtocolVersions:
    """
    Attributes:
        terminal (int):
        desktop (int):
    """

    terminal: int
    desktop: int

    def to_dict(self) -> dict[str, Any]:
        terminal = self.terminal

        desktop = self.desktop

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "terminal": terminal,
                "desktop": desktop,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        terminal = d.pop("terminal")

        desktop = d.pop("desktop")

        machine_protocol_versions = cls(
            terminal=terminal,
            desktop=desktop,
        )

        return machine_protocol_versions
