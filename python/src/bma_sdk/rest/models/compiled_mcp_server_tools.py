from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.compiled_mcp_tool import CompiledMCPTool


T = TypeVar("T", bound="CompiledMCPServerTools")


@_attrs_define
class CompiledMCPServerTools:
    """ """

    additional_properties: dict[str, "CompiledMCPTool"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.compiled_mcp_tool import CompiledMCPTool

        d = dict(src_dict)
        compiled_mcp_server_tools = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = CompiledMCPTool.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        compiled_mcp_server_tools.additional_properties = additional_properties
        return compiled_mcp_server_tools

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "CompiledMCPTool":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "CompiledMCPTool") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
