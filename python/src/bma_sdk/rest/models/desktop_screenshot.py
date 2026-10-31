import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="DesktopScreenshot")


@_attrs_define
class DesktopScreenshot:
    """
    Attributes:
        content_type (str):
        width (int):
        height (int):
        captured_at (datetime.datetime):
        image_base64 (str): Base64-encoded image bytes.
    """

    content_type: str
    width: int
    height: int
    captured_at: datetime.datetime
    image_base64: str

    def to_dict(self) -> dict[str, Any]:
        content_type = self.content_type

        width = self.width

        height = self.height

        captured_at = self.captured_at.isoformat()

        image_base64 = self.image_base64

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "content_type": content_type,
                "width": width,
                "height": height,
                "captured_at": captured_at,
                "image_base64": image_base64,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content_type = d.pop("content_type")

        width = d.pop("width")

        height = d.pop("height")

        captured_at = isoparse(d.pop("captured_at"))

        image_base64 = d.pop("image_base64")

        desktop_screenshot = cls(
            content_type=content_type,
            width=width,
            height=height,
            captured_at=captured_at,
            image_base64=image_base64,
        )

        return desktop_screenshot
