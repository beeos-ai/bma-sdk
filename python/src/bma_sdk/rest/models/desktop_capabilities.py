from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DesktopCapabilities")


@_attrs_define
class DesktopCapabilities:
    """
    Attributes:
        width (int):
        height (int):
        screenshot (bool):
        pointer (bool):
        keyboard (bool):
        text (bool):
        webrtc (bool):
        rfb_fallback (bool):
        takeover (bool):
        max_actions_per_second (int):
        protocol_version (int):
        control_version (int):
        transport_fallback_generation (int):
    """

    width: int
    height: int
    screenshot: bool
    pointer: bool
    keyboard: bool
    text: bool
    webrtc: bool
    rfb_fallback: bool
    takeover: bool
    max_actions_per_second: int
    protocol_version: int
    control_version: int
    transport_fallback_generation: int

    def to_dict(self) -> dict[str, Any]:
        width = self.width

        height = self.height

        screenshot = self.screenshot

        pointer = self.pointer

        keyboard = self.keyboard

        text = self.text

        webrtc = self.webrtc

        rfb_fallback = self.rfb_fallback

        takeover = self.takeover

        max_actions_per_second = self.max_actions_per_second

        protocol_version = self.protocol_version

        control_version = self.control_version

        transport_fallback_generation = self.transport_fallback_generation

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "width": width,
                "height": height,
                "screenshot": screenshot,
                "pointer": pointer,
                "keyboard": keyboard,
                "text": text,
                "webrtc": webrtc,
                "rfb_fallback": rfb_fallback,
                "takeover": takeover,
                "max_actions_per_second": max_actions_per_second,
                "protocol_version": protocol_version,
                "control_version": control_version,
                "transport_fallback_generation": transport_fallback_generation,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        width = d.pop("width")

        height = d.pop("height")

        screenshot = d.pop("screenshot")

        pointer = d.pop("pointer")

        keyboard = d.pop("keyboard")

        text = d.pop("text")

        webrtc = d.pop("webrtc")

        rfb_fallback = d.pop("rfb_fallback")

        takeover = d.pop("takeover")

        max_actions_per_second = d.pop("max_actions_per_second")

        protocol_version = d.pop("protocol_version")

        control_version = d.pop("control_version")

        transport_fallback_generation = d.pop("transport_fallback_generation")

        desktop_capabilities = cls(
            width=width,
            height=height,
            screenshot=screenshot,
            pointer=pointer,
            keyboard=keyboard,
            text=text,
            webrtc=webrtc,
            rfb_fallback=rfb_fallback,
            takeover=takeover,
            max_actions_per_second=max_actions_per_second,
            protocol_version=protocol_version,
            control_version=control_version,
            transport_fallback_generation=transport_fallback_generation,
        )

        return desktop_capabilities
