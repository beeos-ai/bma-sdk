from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="MachineTerminalCapability")


@_attrs_define
class MachineTerminalCapability:
    """
    Attributes:
        supported (bool):
        reason (Union[Unset, str]): Why terminal access is unavailable, when supported is false.
    """

    supported: bool
    reason: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        supported = self.supported

        reason = self.reason

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "supported": supported,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        supported = d.pop("supported")

        reason = d.pop("reason", UNSET)

        machine_terminal_capability = cls(
            supported=supported,
            reason=reason,
        )

        return machine_terminal_capability
