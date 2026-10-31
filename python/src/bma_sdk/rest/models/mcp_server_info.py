from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="MCPServerInfo")


@_attrs_define
class MCPServerInfo:
    """
    Attributes:
        name (str):
        version (str):
        title (Union[Unset, str]):
        description (Union[Unset, str]):
        website_url (Union[Unset, str]):
    """

    name: str
    version: str
    title: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    website_url: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        version = self.version

        title = self.title

        description = self.description

        website_url = self.website_url

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "version": version,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if website_url is not UNSET:
            field_dict["website_url"] = website_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        version = d.pop("version")

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        website_url = d.pop("website_url", UNSET)

        mcp_server_info = cls(
            name=name,
            version=version,
            title=title,
            description=description,
            website_url=website_url,
        )

        return mcp_server_info
