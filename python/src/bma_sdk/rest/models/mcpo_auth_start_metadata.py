from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MCPOAuthStartMetadata")


@_attrs_define
class MCPOAuthStartMetadata:
    """User-supplied metadata for the stored secret. A restriction of Metadata that leaves room for one reserved pair - BMA
    sets mcp_url on the secret to the flow's MCP endpoint URL, so the key is reserved and at most 15 user pairs are
    accepted.

    """

    additional_properties: dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mcpo_auth_start_metadata = cls()

        mcpo_auth_start_metadata.additional_properties = d
        return mcpo_auth_start_metadata

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
