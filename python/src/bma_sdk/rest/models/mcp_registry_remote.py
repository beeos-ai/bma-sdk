from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mcp_registry_header import MCPRegistryHeader


T = TypeVar("T", bound="MCPRegistryRemote")


@_attrs_define
class MCPRegistryRemote:
    """
    Attributes:
        type_ (str): Transport type as published in the registry. Always `streamable-http`; other transports are dropped
            when the snapshot is built.
        url (str):
        headers (Union[Unset, list['MCPRegistryHeader']]):
    """

    type_: str
    url: str
    headers: Union[Unset, list["MCPRegistryHeader"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        url = self.url

        headers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.headers, Unset):
            headers = []
            for headers_item_data in self.headers:
                headers_item = headers_item_data.to_dict()
                headers.append(headers_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "url": url,
            }
        )
        if headers is not UNSET:
            field_dict["headers"] = headers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.mcp_registry_header import MCPRegistryHeader

        d = dict(src_dict)
        type_ = d.pop("type")

        url = d.pop("url")

        headers = []
        _headers = d.pop("headers", UNSET)
        for headers_item_data in _headers or []:
            headers_item = MCPRegistryHeader.from_dict(headers_item_data)

            headers.append(headers_item)

        mcp_registry_remote = cls(
            type_=type_,
            url=url,
            headers=headers,
        )

        return mcp_registry_remote
