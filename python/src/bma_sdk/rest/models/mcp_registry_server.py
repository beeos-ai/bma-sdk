import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mcp_registry_icon import MCPRegistryIcon
    from ..models.mcp_registry_remote import MCPRegistryRemote


T = TypeVar("T", bound="MCPRegistryServer")


@_attrs_define
class MCPRegistryServer:
    """
    Attributes:
        name (str): Reverse-DNS registry name, for example `io.github.owner/server`.
        description (str):
        version (str):
        status (str):
        updated_at (datetime.datetime):
        remotes (list['MCPRegistryRemote']):
        icons (list['MCPRegistryIcon']):
        title (Union[Unset, str]):
        website_url (Union[Unset, str]):
    """

    name: str
    description: str
    version: str
    status: str
    updated_at: datetime.datetime
    remotes: list["MCPRegistryRemote"]
    icons: list["MCPRegistryIcon"]
    title: Union[Unset, str] = UNSET
    website_url: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        version = self.version

        status = self.status

        updated_at = self.updated_at.isoformat()

        remotes = []
        for remotes_item_data in self.remotes:
            remotes_item = remotes_item_data.to_dict()
            remotes.append(remotes_item)

        icons = []
        for icons_item_data in self.icons:
            icons_item = icons_item_data.to_dict()
            icons.append(icons_item)

        title = self.title

        website_url = self.website_url

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "description": description,
                "version": version,
                "status": status,
                "updated_at": updated_at,
                "remotes": remotes,
                "icons": icons,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title
        if website_url is not UNSET:
            field_dict["website_url"] = website_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mcp_registry_icon import MCPRegistryIcon
        from ..models.mcp_registry_remote import MCPRegistryRemote

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        version = d.pop("version")

        status = d.pop("status")

        updated_at = isoparse(d.pop("updated_at"))

        remotes = []
        _remotes = d.pop("remotes")
        for remotes_item_data in _remotes:
            remotes_item = MCPRegistryRemote.from_dict(remotes_item_data)

            remotes.append(remotes_item)

        icons = []
        _icons = d.pop("icons")
        for icons_item_data in _icons:
            icons_item = MCPRegistryIcon.from_dict(icons_item_data)

            icons.append(icons_item)

        title = d.pop("title", UNSET)

        website_url = d.pop("website_url", UNSET)

        mcp_registry_server = cls(
            name=name,
            description=description,
            version=version,
            status=status,
            updated_at=updated_at,
            remotes=remotes,
            icons=icons,
            title=title,
            website_url=website_url,
        )

        return mcp_registry_server
