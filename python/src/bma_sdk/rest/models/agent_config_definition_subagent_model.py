from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.agent_config_definition_subagent_model_cache_retention import (
    AgentConfigDefinitionSubagentModelCacheRetention,
    check_agent_config_definition_subagent_model_cache_retention,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_config_definition_subagent_model_reasoning import (
        AgentConfigDefinitionSubagentModelReasoning,
    )


T = TypeVar("T", bound="AgentConfigDefinitionSubagentModel")


@_attrs_define
class AgentConfigDefinitionSubagentModel:
    """
    Attributes:
        cache_retention (Union[Unset, AgentConfigDefinitionSubagentModelCacheRetention]):
        context_window_tokens (Union[Unset, int]): Context budget for input and output tokens. Triggers compaction when
            estimated input exceeds the remaining budget after output and safety reserves. The turn fails if compaction
            cannot make it fit.
        default_max_output_tokens (Union[Unset, int]):
        name (Union[Unset, str]): Name of an existing resource, resolved when the config is compiled.
        provider_config (Union[Unset, str]): Name of an existing resource, resolved when the config is compiled.
        reasoning (Union[Unset, AgentConfigDefinitionSubagentModelReasoning]):
    """

    cache_retention: Union[Unset, AgentConfigDefinitionSubagentModelCacheRetention] = (
        UNSET
    )
    context_window_tokens: Union[Unset, int] = UNSET
    default_max_output_tokens: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    provider_config: Union[Unset, str] = UNSET
    reasoning: Union[Unset, "AgentConfigDefinitionSubagentModelReasoning"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        cache_retention: Union[Unset, str] = UNSET
        if not isinstance(self.cache_retention, Unset):
            cache_retention = self.cache_retention

        context_window_tokens = self.context_window_tokens

        default_max_output_tokens = self.default_max_output_tokens

        name = self.name

        provider_config = self.provider_config

        reasoning: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.reasoning, Unset):
            reasoning = self.reasoning.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if cache_retention is not UNSET:
            field_dict["cache_retention"] = cache_retention
        if context_window_tokens is not UNSET:
            field_dict["context_window_tokens"] = context_window_tokens
        if default_max_output_tokens is not UNSET:
            field_dict["default_max_output_tokens"] = default_max_output_tokens
        if name is not UNSET:
            field_dict["name"] = name
        if provider_config is not UNSET:
            field_dict["provider_config"] = provider_config
        if reasoning is not UNSET:
            field_dict["reasoning"] = reasoning

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_config_definition_subagent_model_reasoning import (
            AgentConfigDefinitionSubagentModelReasoning,
        )

        d = dict(src_dict)
        _cache_retention = d.pop("cache_retention", UNSET)
        cache_retention: Union[Unset, AgentConfigDefinitionSubagentModelCacheRetention]
        if isinstance(_cache_retention, Unset):
            cache_retention = UNSET
        else:
            cache_retention = (
                check_agent_config_definition_subagent_model_cache_retention(
                    _cache_retention
                )
            )

        context_window_tokens = d.pop("context_window_tokens", UNSET)

        default_max_output_tokens = d.pop("default_max_output_tokens", UNSET)

        name = d.pop("name", UNSET)

        provider_config = d.pop("provider_config", UNSET)

        _reasoning = d.pop("reasoning", UNSET)
        reasoning: Union[Unset, AgentConfigDefinitionSubagentModelReasoning]
        if isinstance(_reasoning, Unset):
            reasoning = UNSET
        else:
            reasoning = AgentConfigDefinitionSubagentModelReasoning.from_dict(
                _reasoning
            )

        agent_config_definition_subagent_model = cls(
            cache_retention=cache_retention,
            context_window_tokens=context_window_tokens,
            default_max_output_tokens=default_max_output_tokens,
            name=name,
            provider_config=provider_config,
            reasoning=reasoning,
        )

        return agent_config_definition_subagent_model
