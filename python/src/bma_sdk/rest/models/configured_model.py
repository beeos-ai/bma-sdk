import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.management_kind import ManagementKind, check_management_kind
from ..models.model_cache_retention import (
    ModelCacheRetention,
    check_model_cache_retention,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.model_api_variant_options import ModelAPIVariantOptions


T = TypeVar("T", bound="ConfiguredModel")


@_attrs_define
class ConfiguredModel:
    """
    Attributes:
        id (str):
        org_id (str):
        model_provider_config_id (str):
        management_kind (ManagementKind): Lifecycle owner. Tenant-managed resources can be changed through tenant APIs.
            Cluster-managed resources are installed and lifecycle-managed by the control plane; individual APIs may
            explicitly expose tenant-editable settings.
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        current_revision_id (str):
        provider_model_slug (str): Exact provider model slug sent to the provider endpoint by the current revision.
        context_window_tokens (int): Context budget for input and output tokens. Triggers compaction when estimated
            input exceeds the remaining budget after output and safety reserves. The turn fails if compaction cannot make it
            fit.
        max_output_tokens (Union[None, int]): Known output-token ceiling for this model, or null when unknown.
        supports_tools (bool): Whether this configured model can receive tool definitions and emit tool calls.
        supports_reasoning (bool): Whether BMA should use this model's reasoning features.
        default_reasoning_effort (str): Default reasoning effort to send for models/API formats that support effort-
            style reasoning controls.
        supported_reasoning_efforts (list[str]): Reasoning effort values this configured model accepts.
        input_modalities (list[str]): Input types this configured model accepts. BMA recognizes text, image, and file;
            an empty list leaves capabilities unspecified.
        output_modalities (list[str]): Output types this configured model can return.
        api_variant_options (ModelAPIVariantOptions): Extra top-level JSON fields to include in provider requests for
            this configured model. Use this for provider-specific settings that BMA does not expose as typed fields, such as
            OpenRouter `provider` routing or sampling parameters. BMA still controls the fields it needs to run the agent
            correctly, including the model, prompt/messages, streaming, tools, output-token limit, and selected reasoning
            policy. Provider passthrough values for those fields are ignored. For OpenRouter routing options, see
            https://openrouter.ai/docs/guides/routing/provider-selection and general request parameters at
            https://openrouter.ai/docs/api/reference/parameters. BMA-managed OpenRouter providers accept only sampling,
            reasoning, and per-model routing options here.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        revision_created_at (datetime.datetime):
        default_max_output_tokens (Union[None, Unset, int]): Default per-request output-token cap sent to the provider
            unless an agent config overrides it.
        default_cache_retention (Union[Unset, ModelCacheRetention]): Prompt-cache preference for model requests; `short`
            when omitted. `short` applies the route's default caching (explicit cache breakpoints where the provider
            requires them) and, where the route accepts one, a stable conversation key for cache-aware routing. `long`
            prefers the route's extended cache lifetime where one exists (currently Anthropic's one-hour cache, which on
            Bedrock requires Claude 4.5 or newer) and behaves like `short` elsewhere. `none` sends no BMA-managed cache
            controls or conversation key; providers may still cache prefixes on their own.
    """

    id: str
    org_id: str
    model_provider_config_id: str
    management_kind: ManagementKind
    name: str
    current_revision_id: str
    provider_model_slug: str
    context_window_tokens: int
    max_output_tokens: Union[None, int]
    supports_tools: bool
    supports_reasoning: bool
    default_reasoning_effort: str
    supported_reasoning_efforts: list[str]
    input_modalities: list[str]
    output_modalities: list[str]
    api_variant_options: "ModelAPIVariantOptions"
    created_at: datetime.datetime
    updated_at: datetime.datetime
    revision_created_at: datetime.datetime
    default_max_output_tokens: Union[None, Unset, int] = UNSET
    default_cache_retention: Union[Unset, ModelCacheRetention] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        model_provider_config_id = self.model_provider_config_id

        management_kind: str = self.management_kind

        name = self.name

        current_revision_id = self.current_revision_id

        provider_model_slug = self.provider_model_slug

        context_window_tokens = self.context_window_tokens

        max_output_tokens: Union[None, int]
        max_output_tokens = self.max_output_tokens

        supports_tools = self.supports_tools

        supports_reasoning = self.supports_reasoning

        default_reasoning_effort = self.default_reasoning_effort

        supported_reasoning_efforts = self.supported_reasoning_efforts

        input_modalities = self.input_modalities

        output_modalities = self.output_modalities

        api_variant_options = self.api_variant_options.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        revision_created_at = self.revision_created_at.isoformat()

        default_max_output_tokens: Union[None, Unset, int]
        if isinstance(self.default_max_output_tokens, Unset):
            default_max_output_tokens = UNSET
        else:
            default_max_output_tokens = self.default_max_output_tokens

        default_cache_retention: Union[Unset, str] = UNSET
        if not isinstance(self.default_cache_retention, Unset):
            default_cache_retention = self.default_cache_retention

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "model_provider_config_id": model_provider_config_id,
                "management_kind": management_kind,
                "name": name,
                "current_revision_id": current_revision_id,
                "provider_model_slug": provider_model_slug,
                "context_window_tokens": context_window_tokens,
                "max_output_tokens": max_output_tokens,
                "supports_tools": supports_tools,
                "supports_reasoning": supports_reasoning,
                "default_reasoning_effort": default_reasoning_effort,
                "supported_reasoning_efforts": supported_reasoning_efforts,
                "input_modalities": input_modalities,
                "output_modalities": output_modalities,
                "api_variant_options": api_variant_options,
                "created_at": created_at,
                "updated_at": updated_at,
                "revision_created_at": revision_created_at,
            }
        )
        if default_max_output_tokens is not UNSET:
            field_dict["default_max_output_tokens"] = default_max_output_tokens
        if default_cache_retention is not UNSET:
            field_dict["default_cache_retention"] = default_cache_retention

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_api_variant_options import ModelAPIVariantOptions

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        model_provider_config_id = d.pop("model_provider_config_id")

        management_kind = check_management_kind(d.pop("management_kind"))

        name = d.pop("name")

        current_revision_id = d.pop("current_revision_id")

        provider_model_slug = d.pop("provider_model_slug")

        context_window_tokens = d.pop("context_window_tokens")

        def _parse_max_output_tokens(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_output_tokens = _parse_max_output_tokens(d.pop("max_output_tokens"))

        supports_tools = d.pop("supports_tools")

        supports_reasoning = d.pop("supports_reasoning")

        default_reasoning_effort = d.pop("default_reasoning_effort")

        supported_reasoning_efforts = cast(
            list[str], d.pop("supported_reasoning_efforts")
        )

        input_modalities = cast(list[str], d.pop("input_modalities"))

        output_modalities = cast(list[str], d.pop("output_modalities"))

        api_variant_options = ModelAPIVariantOptions.from_dict(
            d.pop("api_variant_options")
        )

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        revision_created_at = isoparse(d.pop("revision_created_at"))

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

        configured_model = cls(
            id=id,
            org_id=org_id,
            model_provider_config_id=model_provider_config_id,
            management_kind=management_kind,
            name=name,
            current_revision_id=current_revision_id,
            provider_model_slug=provider_model_slug,
            context_window_tokens=context_window_tokens,
            max_output_tokens=max_output_tokens,
            supports_tools=supports_tools,
            supports_reasoning=supports_reasoning,
            default_reasoning_effort=default_reasoning_effort,
            supported_reasoning_efforts=supported_reasoning_efforts,
            input_modalities=input_modalities,
            output_modalities=output_modalities,
            api_variant_options=api_variant_options,
            created_at=created_at,
            updated_at=updated_at,
            revision_created_at=revision_created_at,
            default_max_output_tokens=default_max_output_tokens,
            default_cache_retention=default_cache_retention,
        )

        return configured_model
