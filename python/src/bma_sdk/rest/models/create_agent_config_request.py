from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..models.create_agent_config_request_source_format import (
    CreateAgentConfigRequestSourceFormat,
    check_create_agent_config_request_source_format,
)

if TYPE_CHECKING:
    from ..models.agent_config_definition import AgentConfigDefinition


T = TypeVar("T", bound="CreateAgentConfigRequest")


@_attrs_define
class CreateAgentConfigRequest:
    """An agent config to compile. YAML sources are stored verbatim, so comments and formatting survive; JSON sources, as
    text or as an object, are stored canonicalized, so the same JSON definition always maps to the same config.

        Attributes:
            source (Union['AgentConfigDefinition', str]): Agent config source as YAML or JSON text, or, with source_format
                json, as a JSON object.
            source_format (CreateAgentConfigRequestSourceFormat): Format of source: yaml or json.
    """

    source: Union["AgentConfigDefinition", str]
    source_format: CreateAgentConfigRequestSourceFormat

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_config_definition import AgentConfigDefinition

        source: Union[dict[str, Any], str]
        if isinstance(self.source, AgentConfigDefinition):
            source = self.source.to_dict()
        else:
            source = self.source

        source_format: str = self.source_format

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "source": source,
                "source_format": source_format,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_definition import AgentConfigDefinition

        d = dict(src_dict)

        def _parse_source(data: object) -> Union["AgentConfigDefinition", str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_agent_config_source_input_type_1 = (
                    AgentConfigDefinition.from_dict(data)
                )

                return componentsschemas_agent_config_source_input_type_1
            except:  # noqa: E722
                pass
            return cast(Union["AgentConfigDefinition", str], data)

        source = _parse_source(d.pop("source"))

        source_format = check_create_agent_config_request_source_format(
            d.pop("source_format")
        )

        create_agent_config_request = cls(
            source=source,
            source_format=source_format,
        )

        return create_agent_config_request
