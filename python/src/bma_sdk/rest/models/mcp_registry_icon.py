from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="MCPRegistryIcon")


@_attrs_define
class MCPRegistryIcon:
    """
    Attributes:
        src (str): Absolute https URL of the icon image.
        mime_type (Union[Unset, str]):
        sizes (Union[Unset, list[str]]): Icon sizes as `WxH` strings, or `any` for scalable images.
        theme (Union[Unset, str]): Theme the icon is intended for, `light` or `dark`, when the publisher specifies one.
    """

    src: str
    mime_type: Union[Unset, str] = UNSET
    sizes: Union[Unset, list[str]] = UNSET
    theme: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        src = self.src

        mime_type = self.mime_type

        sizes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.sizes, Unset):
            sizes = self.sizes

        theme = self.theme

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "src": src,
            }
        )
        if mime_type is not UNSET:
            field_dict["mime_type"] = mime_type
        if sizes is not UNSET:
            field_dict["sizes"] = sizes
        if theme is not UNSET:
            field_dict["theme"] = theme

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        src = d.pop("src")

        mime_type = d.pop("mime_type", UNSET)

        sizes = cast(list[str], d.pop("sizes", UNSET))

        theme = d.pop("theme", UNSET)

        mcp_registry_icon = cls(
            src=src,
            mime_type=mime_type,
            sizes=sizes,
            theme=theme,
        )

        return mcp_registry_icon
