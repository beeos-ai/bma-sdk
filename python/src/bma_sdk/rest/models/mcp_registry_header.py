from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="MCPRegistryHeader")


@_attrs_define
class MCPRegistryHeader:
    """
    Attributes:
        name (str):
        is_required (bool):
        is_secret (bool):
        description (Union[Unset, str]):
    """

    name: str
    is_required: bool
    is_secret: bool
    description: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        is_required = self.is_required

        is_secret = self.is_secret

        description = self.description

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "is_required": is_required,
                "is_secret": is_secret,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        is_required = d.pop("is_required")

        is_secret = d.pop("is_secret")

        description = d.pop("description", UNSET)

        mcp_registry_header = cls(
            name=name,
            is_required=is_required,
            is_secret=is_secret,
            description=description,
        )

        return mcp_registry_header
