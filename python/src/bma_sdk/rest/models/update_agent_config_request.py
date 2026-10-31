from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..models.update_agent_config_request_source_format import (
    UpdateAgentConfigRequestSourceFormat,
    check_update_agent_config_request_source_format,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config_definition import AgentConfigDefinition


T = TypeVar("T", bound="UpdateAgentConfigRequest")


@_attrs_define
class UpdateAgentConfigRequest:
    """Replaces a live agent's config. expected_current_config_id makes the change conditional on the agent still running
    that config, so concurrent editors get a conflict instead of silently overwriting each other.

        Attributes:
            source (Union['AgentConfigDefinition', str]): Agent config source as YAML or JSON text, or, with source_format
                json, as a JSON object.
            source_format (UpdateAgentConfigRequestSourceFormat): Format of source: yaml or json.
            expected_current_config_id (Union[Unset, str]): Agent config ID (acfg_...).
    """

    source: Union["AgentConfigDefinition", str]
    source_format: UpdateAgentConfigRequestSourceFormat
    expected_current_config_id: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_config_definition import AgentConfigDefinition

        source: Union[dict[str, Any], str]
        if isinstance(self.source, AgentConfigDefinition):
            source = self.source.to_dict()
        else:
            source = self.source

        source_format: str = self.source_format

        expected_current_config_id = self.expected_current_config_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "source": source,
                "source_format": source_format,
            }
        )
        if expected_current_config_id is not UNSET:
            field_dict["expected_current_config_id"] = expected_current_config_id

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

        source_format = check_update_agent_config_request_source_format(
            d.pop("source_format")
        )

        expected_current_config_id = d.pop("expected_current_config_id", UNSET)

        update_agent_config_request = cls(
            source=source,
            source_format=source_format,
            expected_current_config_id=expected_current_config_id,
        )

        return update_agent_config_request
