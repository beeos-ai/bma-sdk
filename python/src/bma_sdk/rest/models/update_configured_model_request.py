from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..models.model_cache_retention import (
    ModelCacheRetention,
    check_model_cache_retention,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_api_variant_options import ModelAPIVariantOptions


T = TypeVar("T", bound="UpdateConfiguredModelRequest")


@_attrs_define
class UpdateConfiguredModelRequest:
    """Update a configured model. Omitted fields keep their current values. Runtime changes create a new immutable model
    revision; changing only name just renames the model.

        Attributes:
            name (Union[Unset, str]): Human-readable name. Spaces and punctuation are allowed; leading or trailing
                whitespace and invisible or control characters are not.
            provider_model_slug (Union[Unset, str]): Exact provider model slug sent to the provider endpoint. Free-pool,
                `:online`, and preset model ids are not accepted on BMA-managed OpenRouter providers.
            context_window_tokens (Union[Unset, int]): Context budget for input and output tokens. Triggers compaction when
                estimated input exceeds the remaining budget after output and safety reserves. The turn fails if compaction
                cannot make it fit.
            max_output_tokens (Union[None, Unset, int]): Known output-token ceiling for this model. Omitted keeps the
                current value. Null clears it to unknown for every API format.
            default_max_output_tokens (Union[None, Unset, int]): Optional per-request output allowance unless a project or
                agent overrides it. Without a default or known ceiling, Messages uses 64000 tokens; other formats omit the
                allowance.
            default_cache_retention (Union[Unset, ModelCacheRetention]): Prompt-cache preference for model requests; `short`
                when omitted. `short` applies the route's default caching (explicit cache breakpoints where the provider
                requires them) and, where the route accepts one, a stable conversation key for cache-aware routing. `long`
                prefers the route's extended cache lifetime where one exists (currently Anthropic's one-hour cache, which on
                Bedrock requires Claude 4.5 or newer) and behaves like `short` elsewhere. `none` sends no BMA-managed cache
                controls or conversation key; providers may still cache prefixes on their own.
            supports_tools (Union[Unset, bool]): Whether this configured model can receive tool definitions and emit tool
                calls. Agent configs with enabled tools are rejected when this is false. Omitted keeps the current value.
            supports_reasoning (Union[Unset, bool]): Whether BMA should use this model's reasoning features. For OpenAI
                Responses, this also enables encrypted reasoning replay for stateless calls. Omitted keeps the current value.
            default_reasoning_effort (Union[Unset, str]): Default reasoning effort to send for models/API formats that
                support effort-style reasoning controls. Requires supports_reasoning=true. When supported_reasoning_efforts is
                present, this value must be listed there.
            supported_reasoning_efforts (Union[Unset, list[str]]): Reasoning effort values this configured model accepts.
                Requires supports_reasoning=true when non-empty.
            input_modalities (Union[Unset, list[str]]): Input types this configured model accepts. BMA recognizes text,
                image, and file; an empty list leaves capabilities unspecified.
            output_modalities (Union[Unset, list[str]]): Output types this configured model can return. BMA currently
                consumes text output.
            api_variant_options (Union[Unset, ModelAPIVariantOptions]): Extra top-level JSON fields to include in provider
                requests for this configured model. Use this for provider-specific settings that BMA does not expose as typed
                fields, such as OpenRouter `provider` routing or sampling parameters. BMA still controls the fields it needs to
                run the agent correctly, including the model, prompt/messages, streaming, tools, output-token limit, and
                selected reasoning policy. Provider passthrough values for those fields are ignored. For OpenRouter routing
                options, see https://openrouter.ai/docs/guides/routing/provider-selection and general request parameters at
                https://openrouter.ai/docs/api/reference/parameters. BMA-managed OpenRouter providers accept only sampling,
                reasoning, and per-model routing options here.
    """

    name: Union[Unset, str] = UNSET
    provider_model_slug: Union[Unset, str] = UNSET
    context_window_tokens: Union[Unset, int] = UNSET
    max_output_tokens: Union[None, Unset, int] = UNSET
    default_max_output_tokens: Union[None, Unset, int] = UNSET
    default_cache_retention: Union[Unset, ModelCacheRetention] = UNSET
    supports_tools: Union[Unset, bool] = UNSET
    supports_reasoning: Union[Unset, bool] = UNSET
    default_reasoning_effort: Union[Unset, str] = UNSET
    supported_reasoning_efforts: Union[Unset, list[str]] = UNSET
    input_modalities: Union[Unset, list[str]] = UNSET
    output_modalities: Union[Unset, list[str]] = UNSET
    api_variant_options: Union[Unset, "ModelAPIVariantOptions"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        provider_model_slug = self.provider_model_slug

        context_window_tokens = self.context_window_tokens

        max_output_tokens: Union[None, Unset, int]
        if isinstance(self.max_output_tokens, Unset):
            max_output_tokens = UNSET
        else:
            max_output_tokens = self.max_output_tokens

        default_max_output_tokens: Union[None, Unset, int]
        if isinstance(self.default_max_output_tokens, Unset):
            default_max_output_tokens = UNSET
        else:
            default_max_output_tokens = self.default_max_output_tokens

        default_cache_retention: Union[Unset, str] = UNSET
        if not isinstance(self.default_cache_retention, Unset):
            default_cache_retention = self.default_cache_retention

        supports_tools = self.supports_tools

        supports_reasoning = self.supports_reasoning

        default_reasoning_effort = self.default_reasoning_effort

        supported_reasoning_efforts: Union[Unset, list[str]] = UNSET
        if not isinstance(self.supported_reasoning_efforts, Unset):
            supported_reasoning_efforts = self.supported_reasoning_efforts

        input_modalities: Union[Unset, list[str]] = UNSET
        if not isinstance(self.input_modalities, Unset):
            input_modalities = self.input_modalities

        output_modalities: Union[Unset, list[str]] = UNSET
        if not isinstance(self.output_modalities, Unset):
            output_modalities = self.output_modalities

        api_variant_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.api_variant_options, Unset):
            api_variant_options = self.api_variant_options.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if provider_model_slug is not UNSET:
            field_dict["provider_model_slug"] = provider_model_slug
        if context_window_tokens is not UNSET:
            field_dict["context_window_tokens"] = context_window_tokens
        if max_output_tokens is not UNSET:
            field_dict["max_output_tokens"] = max_output_tokens
        if default_max_output_tokens is not UNSET:
            field_dict["default_max_output_tokens"] = default_max_output_tokens
        if default_cache_retention is not UNSET:
            field_dict["default_cache_retention"] = default_cache_retention
        if supports_tools is not UNSET:
            field_dict["supports_tools"] = supports_tools
        if supports_reasoning is not UNSET:
            field_dict["supports_reasoning"] = supports_reasoning
        if default_reasoning_effort is not UNSET:
            field_dict["default_reasoning_effort"] = default_reasoning_effort
        if supported_reasoning_efforts is not UNSET:
            field_dict["supported_reasoning_efforts"] = supported_reasoning_efforts
        if input_modalities is not UNSET:
            field_dict["input_modalities"] = input_modalities
        if output_modalities is not UNSET:
            field_dict["output_modalities"] = output_modalities
        if api_variant_options is not UNSET:
            field_dict["api_variant_options"] = api_variant_options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_api_variant_options import ModelAPIVariantOptions

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        provider_model_slug = d.pop("provider_model_slug", UNSET)

        context_window_tokens = d.pop("context_window_tokens", UNSET)

        def _parse_max_output_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_output_tokens = _parse_max_output_tokens(d.pop("max_output_tokens", UNSET))

        def _parse_default_max_output_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        default_max_output_tokens = _parse_default_max_output_tokens(
            d.pop("default_max_output_tokens", UNSET)
        )

        _default_cache_retention = d.pop("default_cache_retention", UNSET)
        default_cache_retention: Union[Unset, ModelCacheRetention]
        if isinstance(_default_cache_retention, Unset):
            default_cache_retention = UNSET
        else:
            default_cache_retention = check_model_cache_retention(
                _default_cache_retention
            )

        supports_tools = d.pop("supports_tools", UNSET)

        supports_reasoning = d.pop("supports_reasoning", UNSET)

        default_reasoning_effort = d.pop("default_reasoning_effort", UNSET)

        supported_reasoning_efforts = cast(
            list[str], d.pop("supported_reasoning_efforts", UNSET)
        )

        input_modalities = cast(list[str], d.pop("input_modalities", UNSET))

        output_modalities = cast(list[str], d.pop("output_modalities", UNSET))

        _api_variant_options = d.pop("api_variant_options", UNSET)
        api_variant_options: Union[Unset, ModelAPIVariantOptions]
        if isinstance(_api_variant_options, Unset):
            api_variant_options = UNSET
        else:
            api_variant_options = ModelAPIVariantOptions.from_dict(_api_variant_options)

        update_configured_model_request = cls(
            name=name,
            provider_model_slug=provider_model_slug,
            context_window_tokens=context_window_tokens,
            max_output_tokens=max_output_tokens,
            default_max_output_tokens=default_max_output_tokens,
            default_cache_retention=default_cache_retention,
            supports_tools=supports_tools,
            supports_reasoning=supports_reasoning,
            default_reasoning_effort=default_reasoning_effort,
            supported_reasoning_efforts=supported_reasoning_efforts,
            input_modalities=input_modalities,
            output_modalities=output_modalities,
            api_variant_options=api_variant_options,
        )

        return update_configured_model_request
