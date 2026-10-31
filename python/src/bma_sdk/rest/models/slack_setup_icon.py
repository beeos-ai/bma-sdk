from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="SlackSetupIcon")


@_attrs_define
class SlackSetupIcon:
    """
    Attributes:
        data_base64 (str):
        filename (Union[Unset, str]):
    """

    data_base64: str
    filename: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        data_base64 = self.data_base64

        filename = self.filename

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data_base64": data_base64,
            }
        )
        if filename is not UNSET:
            field_dict["filename"] = filename

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        data_base64 = d.pop("data_base64")

        filename = d.pop("filename", UNSET)

        slack_setup_icon = cls(
            data_base64=data_base64,
            filename=filename,
        )

        return slack_setup_icon
