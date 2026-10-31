from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..models.resolve_agent_config_tools_request_source_format import (
    ResolveAgentConfigToolsRequestSourceFormat,
    check_resolve_agent_config_tools_request_source_format,
)

if TYPE_CHECKING:
    from ..models.agent_config_tools_definition import AgentConfigToolsDefinition


T = TypeVar("T", bound="ResolveAgentConfigToolsRequest")


@_attrs_define
class ResolveAgentConfigToolsRequest:
    """
    Attributes:
        source (Union['AgentConfigToolsDefinition', str]): Agent config source as YAML or JSON text, or, with
            source_format json, as a JSON object. Only the fields that determine tools are read.
        source_format (ResolveAgentConfigToolsRequestSourceFormat):
    """

    source: Union["AgentConfigToolsDefinition", str]
    source_format: ResolveAgentConfigToolsRequestSourceFormat

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_config_tools_definition import AgentConfigToolsDefinition

        source: Union[dict[str, Any], str]
        if isinstance(self.source, AgentConfigToolsDefinition):
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
        from ..models.agent_config_tools_definition import AgentConfigToolsDefinition

        d = dict(src_dict)

        def _parse_source(data: object) -> Union["AgentConfigToolsDefinition", str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                source_type_1 = AgentConfigToolsDefinition.from_dict(data)

                return source_type_1
            except:  # noqa: E722
                pass
            return cast(Union["AgentConfigToolsDefinition", str], data)

        source = _parse_source(d.pop("source"))

        source_format = check_resolve_agent_config_tools_request_source_format(
            d.pop("source_format")
        )

        resolve_agent_config_tools_request = cls(
            source=source,
            source_format=source_format,
        )

        return resolve_agent_config_tools_request
