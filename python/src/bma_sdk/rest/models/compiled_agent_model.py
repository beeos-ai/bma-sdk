from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.model_cache_retention import (
    ModelCacheRetention,
    check_model_cache_retention,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.compiled_model_reasoning import CompiledModelReasoning


T = TypeVar("T", bound="CompiledAgentModel")


@_attrs_define
class CompiledAgentModel:
    """
    Attributes:
        configured_model_id (str):
        context_window_tokens (Union[Unset, int]):
        default_max_output_tokens (Union[Unset, int]):
        cache_retention (Union[Unset, ModelCacheRetention]): Prompt-cache preference for model requests; `short` when
            omitted. `short` applies the route's default caching (explicit cache breakpoints where the provider requires
            them) and, where the route accepts one, a stable conversation key for cache-aware routing. `long` prefers the
            route's extended cache lifetime where one exists (currently Anthropic's one-hour cache, which on Bedrock
            requires Claude 4.5 or newer) and behaves like `short` elsewhere. `none` sends no BMA-managed cache controls or
            conversation key; providers may still cache prefixes on their own.
        reasoning (Union[Unset, CompiledModelReasoning]):
    """

    configured_model_id: str
    context_window_tokens: Union[Unset, int] = UNSET
    default_max_output_tokens: Union[Unset, int] = UNSET
    cache_retention: Union[Unset, ModelCacheRetention] = UNSET
    reasoning: Union[Unset, "CompiledModelReasoning"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        configured_model_id = self.configured_model_id

        context_window_tokens = self.context_window_tokens

        default_max_output_tokens = self.default_max_output_tokens

        cache_retention: Union[Unset, str] = UNSET
        if not isinstance(self.cache_retention, Unset):
            cache_retention = self.cache_retention

        reasoning: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.reasoning, Unset):
            reasoning = self.reasoning.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "configured_model_id": configured_model_id,
            }
        )
        if context_window_tokens is not UNSET:
            field_dict["context_window_tokens"] = context_window_tokens
        if default_max_output_tokens is not UNSET:
            field_dict["default_max_output_tokens"] = default_max_output_tokens
        if cache_retention is not UNSET:
            field_dict["cache_retention"] = cache_retention
        if reasoning is not UNSET:
            field_dict["reasoning"] = reasoning

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.compiled_model_reasoning import CompiledModelReasoning

        d = dict(src_dict)
        configured_model_id = d.pop("configured_model_id")

        context_window_tokens = d.pop("context_window_tokens", UNSET)

        default_max_output_tokens = d.pop("default_max_output_tokens", UNSET)

        _cache_retention = d.pop("cache_retention", UNSET)
        cache_retention: Union[Unset, ModelCacheRetention]
        if isinstance(_cache_retention, Unset):
            cache_retention = UNSET
        else:
            cache_retention = check_model_cache_retention(_cache_retention)

        _reasoning = d.pop("reasoning", UNSET)
        reasoning: Union[Unset, CompiledModelReasoning]
        if isinstance(_reasoning, Unset):
            reasoning = UNSET
        else:
            reasoning = CompiledModelReasoning.from_dict(_reasoning)

        compiled_agent_model = cls(
            configured_model_id=configured_model_id,
            context_window_tokens=context_window_tokens,
            default_max_output_tokens=default_max_output_tokens,
            cache_retention=cache_retention,
            reasoning=reasoning,
        )

        return compiled_agent_model
