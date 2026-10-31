from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DesktopCapabilitiesRequest")


@_attrs_define
class DesktopCapabilitiesRequest:
    """
    Attributes:
        width (Union[Unset, int]): Framebuffer width in pixels. Set together with height; 1280x800 when both are
            omitted. Values outside 640..1920 are rejected at create time.
        height (Union[Unset, int]): Framebuffer height in pixels. Set together with width; 800 when both are omitted.
            Values outside 480..1080 are rejected at create time.
        screenshot (Union[Unset, bool]):
        pointer (Union[Unset, bool]):
        keyboard (Union[Unset, bool]):
        text (Union[Unset, bool]):
        webrtc (Union[Unset, bool]):
        rfb_fallback (Union[Unset, bool]):
        takeover (Union[Unset, bool]):
    """

    width: Union[Unset, int] = UNSET
    height: Union[Unset, int] = UNSET
    screenshot: Union[Unset, bool] = UNSET
    pointer: Union[Unset, bool] = UNSET
    keyboard: Union[Unset, bool] = UNSET
    text: Union[Unset, bool] = UNSET
    webrtc: Union[Unset, bool] = UNSET
    rfb_fallback: Union[Unset, bool] = UNSET
    takeover: Union[Unset, bool] = UNSET

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

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if width is not UNSET:
            field_dict["width"] = width
        if height is not UNSET:
            field_dict["height"] = height
        if screenshot is not UNSET:
            field_dict["screenshot"] = screenshot
        if pointer is not UNSET:
            field_dict["pointer"] = pointer
        if keyboard is not UNSET:
            field_dict["keyboard"] = keyboard
        if text is not UNSET:
            field_dict["text"] = text
        if webrtc is not UNSET:
            field_dict["webrtc"] = webrtc
        if rfb_fallback is not UNSET:
            field_dict["rfb_fallback"] = rfb_fallback
        if takeover is not UNSET:
            field_dict["takeover"] = takeover

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        width = d.pop("width", UNSET)

        height = d.pop("height", UNSET)

        screenshot = d.pop("screenshot", UNSET)

        pointer = d.pop("pointer", UNSET)

        keyboard = d.pop("keyboard", UNSET)

        text = d.pop("text", UNSET)

        webrtc = d.pop("webrtc", UNSET)

        rfb_fallback = d.pop("rfb_fallback", UNSET)

        takeover = d.pop("takeover", UNSET)

        desktop_capabilities_request = cls(
            width=width,
            height=height,
            screenshot=screenshot,
            pointer=pointer,
            keyboard=keyboard,
            text=text,
            webrtc=webrtc,
            rfb_fallback=rfb_fallback,
            takeover=takeover,
        )

        return desktop_capabilities_request
