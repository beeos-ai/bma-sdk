from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.create_agent_config_request import CreateAgentConfigRequest


T = TypeVar("T", bound="CreateAgentRequestType2")


@_attrs_define
class CreateAgentRequestType2:
    """
    Attributes:
        config_source (CreateAgentConfigRequest): An agent config to compile. YAML sources are stored verbatim, so
            comments and formatting survive; JSON sources, as text or as an object, are stored canonicalized, so the same
            JSON definition always maps to the same config.
    """

    config_source: "CreateAgentConfigRequest"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        config_source = self.config_source.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "config_source": config_source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_agent_config_request import CreateAgentConfigRequest

        d = dict(src_dict)
        config_source = CreateAgentConfigRequest.from_dict(d.pop("config_source"))

        create_agent_request_type_2 = cls(
            config_source=config_source,
        )

        create_agent_request_type_2.additional_properties = d
        return create_agent_request_type_2

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
