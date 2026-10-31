from collections.abc import Mapping
from typing import (
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

T = TypeVar("T", bound="CreateProjectModelGrantRequest")


@_attrs_define
class CreateProjectModelGrantRequest:
    """Grant a project access to a configured model. Optional fields can narrow the model's limits for this project;
    omitted fields inherit from the org-level configured model.

        Attributes:
            configured_model_id (str):
            context_window_tokens (Union[Unset, int]): Optional project context budget for input and output tokens. Cannot
                exceed the configured model's budget. Triggers compaction when estimated input exceeds the remaining budget
                after output and safety reserves. The turn fails if compaction cannot make it fit.
            max_output_tokens (Union[Unset, int]): Optional project output-token ceiling. Cannot exceed the configured
                model's ceiling.
            default_max_output_tokens (Union[Unset, int]): Optional project default per-request output-token cap.
            default_cache_retention (Union[Unset, ModelCacheRetention]): Prompt-cache preference for model requests; `short`
                when omitted. `short` applies the route's default caching (explicit cache breakpoints where the provider
                requires them) and, where the route accepts one, a stable conversation key for cache-aware routing. `long`
                prefers the route's extended cache lifetime where one exists (currently Anthropic's one-hour cache, which on
                Bedrock requires Claude 4.5 or newer) and behaves like `short` elsewhere. `none` sends no BMA-managed cache
                controls or conversation key; providers may still cache prefixes on their own.
            supports_tools (Union[Unset, bool]): Optional project-level tool-use gate. Can disable tools, but cannot enable
                tools when the configured model does not support them.
            supports_reasoning (Union[Unset, bool]): Optional project-level reasoning gate. Can disable reasoning, but
                cannot enable reasoning when the configured model does not support it.
            default_reasoning_effort (Union[Unset, str]): Optional project default reasoning effort.
            supported_reasoning_efforts (Union[Unset, list[str]]): Optional project subset of configured-model reasoning
                efforts. If this excludes the inherited default_reasoning_effort, set default_reasoning_effort on the grant too.
            input_modalities (Union[Unset, list[str]]): Optional project subset of configured-model input types (text,
                image, or file). Empty or omitted means inherit.
            output_modalities (Union[Unset, list[str]]): Optional project subset of configured-model output types. Empty or
                omitted means inherit.
    """

    configured_model_id: str
    context_window_tokens: Union[Unset, int] = UNSET
    max_output_tokens: Union[Unset, int] = UNSET
    default_max_output_tokens: Union[Unset, int] = UNSET
    default_cache_retention: Union[Unset, ModelCacheRetention] = UNSET
    supports_tools: Union[Unset, bool] = UNSET
    supports_reasoning: Union[Unset, bool] = UNSET
    default_reasoning_effort: Union[Unset, str] = UNSET
    supported_reasoning_efforts: Union[Unset, list[str]] = UNSET
    input_modalities: Union[Unset, list[str]] = UNSET
    output_modalities: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        configured_model_id = self.configured_model_id

        context_window_tokens = self.context_window_tokens

        max_output_tokens = self.max_output_tokens

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

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "configured_model_id": configured_model_id,
            }
        )
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        configured_model_id = d.pop("configured_model_id")

        context_window_tokens = d.pop("context_window_tokens", UNSET)

        max_output_tokens = d.pop("max_output_tokens", UNSET)

        default_max_output_tokens = d.pop("default_max_output_tokens", UNSET)

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

        create_project_model_grant_request = cls(
            configured_model_id=configured_model_id,
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
        )

        return create_project_model_grant_request
