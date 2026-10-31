from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..models.model_api_format import ModelAPIFormat, check_model_api_format
from ..models.model_cache_retention import (
    ModelCacheRetention,
    check_model_cache_retention,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentConfigModel")


@_attrs_define
class AgentConfigModel:
    """
    Attributes:
        provider_config (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace
            and invisible or control characters are not.
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        provider_model_slug (str): Exact provider model slug on the configured model's current revision at response
            time.
        configured_model_id (str):
        current_revision_id (str):
        api_format (ModelAPIFormat): Wire protocol the model endpoint speaks: openai-responses, openai-chat-completions,
            or anthropic-messages.
        api_variant (str):
        context_window_tokens (int): Effective context budget for input and output tokens after model, project, and
            agent settings are applied. Triggers compaction when estimated input exceeds the remaining budget after output
            and safety reserves. The turn fails if compaction cannot make it fit.
        max_output_tokens (Union[None, int]): Effective known output-token ceiling after model and project settings, or
            null when unknown.
        default_cache_retention (ModelCacheRetention): Prompt-cache preference for model requests; `short` when omitted.
            `short` applies the route's default caching (explicit cache breakpoints where the provider requires them) and,
            where the route accepts one, a stable conversation key for cache-aware routing. `long` prefers the route's
            extended cache lifetime where one exists (currently Anthropic's one-hour cache, which on Bedrock requires Claude
            4.5 or newer) and behaves like `short` elsewhere. `none` sends no BMA-managed cache controls or conversation
            key; providers may still cache prefixes on their own.
        supports_tools (bool):
        supports_reasoning (bool):
        default_reasoning_effort (str):
        supported_reasoning_efforts (list[str]):
        input_modalities (list[str]):
        output_modalities (list[str]):
        default_max_output_tokens (Union[None, Unset, int]): Effective per-request output-token cap sent to the
            provider.
    """

    provider_config: str
    name: str
    provider_model_slug: str
    configured_model_id: str
    current_revision_id: str
    api_format: ModelAPIFormat
    api_variant: str
    context_window_tokens: int
    max_output_tokens: Union[None, int]
    default_cache_retention: ModelCacheRetention
    supports_tools: bool
    supports_reasoning: bool
    default_reasoning_effort: str
    supported_reasoning_efforts: list[str]
    input_modalities: list[str]
    output_modalities: list[str]
    default_max_output_tokens: Union[None, Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        provider_config = self.provider_config

        name = self.name

        provider_model_slug = self.provider_model_slug

        configured_model_id = self.configured_model_id

        current_revision_id = self.current_revision_id

        api_format: str = self.api_format

        api_variant = self.api_variant

        context_window_tokens = self.context_window_tokens

        max_output_tokens: Union[None, int]
        max_output_tokens = self.max_output_tokens

        default_cache_retention: str = self.default_cache_retention

        supports_tools = self.supports_tools

        supports_reasoning = self.supports_reasoning

        default_reasoning_effort = self.default_reasoning_effort

        supported_reasoning_efforts = self.supported_reasoning_efforts

        input_modalities = self.input_modalities

        output_modalities = self.output_modalities

        default_max_output_tokens: Union[None, Unset, int]
        if isinstance(self.default_max_output_tokens, Unset):
            default_max_output_tokens = UNSET
        else:
            default_max_output_tokens = self.default_max_output_tokens

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "provider_config": provider_config,
                "name": name,
                "provider_model_slug": provider_model_slug,
                "configured_model_id": configured_model_id,
                "current_revision_id": current_revision_id,
                "api_format": api_format,
                "api_variant": api_variant,
                "context_window_tokens": context_window_tokens,
                "max_output_tokens": max_output_tokens,
                "default_cache_retention": default_cache_retention,
                "supports_tools": supports_tools,
                "supports_reasoning": supports_reasoning,
                "default_reasoning_effort": default_reasoning_effort,
                "supported_reasoning_efforts": supported_reasoning_efforts,
                "input_modalities": input_modalities,
                "output_modalities": output_modalities,
            }
        )
        if default_max_output_tokens is not UNSET:
            field_dict["default_max_output_tokens"] = default_max_output_tokens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider_config = d.pop("provider_config")

        name = d.pop("name")

        provider_model_slug = d.pop("provider_model_slug")

        configured_model_id = d.pop("configured_model_id")

        current_revision_id = d.pop("current_revision_id")

        api_format = check_model_api_format(d.pop("api_format"))

        api_variant = d.pop("api_variant")

        context_window_tokens = d.pop("context_window_tokens")

        def _parse_max_output_tokens(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_output_tokens = _parse_max_output_tokens(d.pop("max_output_tokens"))

        default_cache_retention = check_model_cache_retention(
            d.pop("default_cache_retention")
        )

        supports_tools = d.pop("supports_tools")

        supports_reasoning = d.pop("supports_reasoning")

        default_reasoning_effort = d.pop("default_reasoning_effort")

        supported_reasoning_efforts = cast(
            list[str], d.pop("supported_reasoning_efforts")
        )

        input_modalities = cast(list[str], d.pop("input_modalities"))

        output_modalities = cast(list[str], d.pop("output_modalities"))

        def _parse_default_max_output_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        default_max_output_tokens = _parse_default_max_output_tokens(
            d.pop("default_max_output_tokens", UNSET)
        )

        agent_config_model = cls(
            provider_config=provider_config,
            name=name,
            provider_model_slug=provider_model_slug,
            configured_model_id=configured_model_id,
            current_revision_id=current_revision_id,
            api_format=api_format,
            api_variant=api_variant,
            context_window_tokens=context_window_tokens,
            max_output_tokens=max_output_tokens,
            default_cache_retention=default_cache_retention,
            supports_tools=supports_tools,
            supports_reasoning=supports_reasoning,
            default_reasoning_effort=default_reasoning_effort,
            supported_reasoning_efforts=supported_reasoning_efforts,
            input_modalities=input_modalities,
            output_modalities=output_modalities,
            default_max_output_tokens=default_max_output_tokens,
        )

        return agent_config_model
