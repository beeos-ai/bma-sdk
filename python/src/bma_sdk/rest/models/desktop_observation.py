from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.desktop_control_status import DesktopControlStatus


T = TypeVar("T", bound="DesktopObservation")


@_attrs_define
class DesktopObservation:
    """
    Attributes:
        control (DesktopControlStatus):
        bytes_ (int):
        width (int):
        height (int):
        content_type (str):
    """

    control: "DesktopControlStatus"
    bytes_: int
    width: int
    height: int
    content_type: str

    def to_dict(self) -> dict[str, Any]:
        control = self.control.to_dict()

        bytes_ = self.bytes_

        width = self.width

        height = self.height

        content_type = self.content_type

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "control": control,
                "bytes": bytes_,
                "width": width,
                "height": height,
                "content_type": content_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.desktop_control_status import DesktopControlStatus

        d = dict(src_dict)
        control = DesktopControlStatus.from_dict(d.pop("control"))

        bytes_ = d.pop("bytes")

        width = d.pop("width")

        height = d.pop("height")

        content_type = d.pop("content_type")

        desktop_observation = cls(
            control=control,
            bytes_=bytes_,
            width=width,
            height=height,
            content_type=content_type,
        )

        return desktop_observation
