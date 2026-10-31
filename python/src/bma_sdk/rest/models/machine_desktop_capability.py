from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="MachineDesktopCapability")


@_attrs_define
class MachineDesktopCapability:
    """
    Attributes:
        supported (bool):
        webrtc (bool):
        rfb (bool):
        reason (Union[Unset, str]): Why desktop access is unavailable, when supported is false.
    """

    supported: bool
    webrtc: bool
    rfb: bool
    reason: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        supported = self.supported

        webrtc = self.webrtc

        rfb = self.rfb

        reason = self.reason

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "supported": supported,
                "webrtc": webrtc,
                "rfb": rfb,
            }
        )
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        supported = d.pop("supported")

        webrtc = d.pop("webrtc")

        rfb = d.pop("rfb")

        reason = d.pop("reason", UNSET)

        machine_desktop_capability = cls(
            supported=supported,
            webrtc=webrtc,
            rfb=rfb,
            reason=reason,
        )

        return machine_desktop_capability
