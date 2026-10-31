from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.compiled_profile_subagent import CompiledProfileSubagent
    from ..models.compiled_self_subagent import CompiledSelfSubagent


T = TypeVar("T", bound="CompiledAgentConfigSubagents")


@_attrs_define
class CompiledAgentConfigSubagents:
    """ """

    additional_properties: dict[
        str, Union["CompiledProfileSubagent", "CompiledSelfSubagent"]
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.compiled_self_subagent import CompiledSelfSubagent

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, CompiledSelfSubagent):
                field_dict[prop_name] = prop.to_dict()
            else:
                field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.compiled_profile_subagent import CompiledProfileSubagent
        from ..models.compiled_self_subagent import CompiledSelfSubagent

        d = dict(src_dict)
        compiled_agent_config_subagents = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> Union["CompiledProfileSubagent", "CompiledSelfSubagent"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_compiled_subagent_type_0 = (
                        CompiledSelfSubagent.from_dict(data)
                    )

                    return componentsschemas_compiled_subagent_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_compiled_subagent_type_1 = (
                    CompiledProfileSubagent.from_dict(data)
                )

                return componentsschemas_compiled_subagent_type_1

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        compiled_agent_config_subagents.additional_properties = additional_properties
        return compiled_agent_config_subagents

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(
        self, key: str
    ) -> Union["CompiledProfileSubagent", "CompiledSelfSubagent"]:
        return self.additional_properties[key]

    def __setitem__(
        self, key: str, value: Union["CompiledProfileSubagent", "CompiledSelfSubagent"]
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
