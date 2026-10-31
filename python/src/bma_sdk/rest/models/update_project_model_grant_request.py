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

T = TypeVar("T", bound="UpdateProjectModelGrantRequest")


@_attrs_define
class UpdateProjectModelGrantRequest:
    """Update a project model grant's overrides. Omitted fields keep their current values. Null clears an override so the
    project inherits from the configured model; for arrays, an empty array clears the override.

        Attributes:
            context_window_tokens (Union[None, Unset, int]): Project context budget for input and output tokens. Cannot
                exceed the configured model's budget. Triggers compaction when estimated input exceeds the remaining budget
                after output and safety reserves. The turn fails if compaction cannot make it fit.
            max_output_tokens (Union[None, Unset, int]): Project output-token ceiling. Cannot exceed the configured model's
                ceiling.
            default_max_output_tokens (Union[None, Unset, int]): Project default per-request output-token cap.
            default_cache_retention (Union[ModelCacheRetention, None, Unset]):
            supports_tools (Union[None, Unset, bool]): Project-level tool-use gate. Can disable tools, but cannot enable
                tools when the configured model does not support them.
            supports_reasoning (Union[None, Unset, bool]): Project-level reasoning gate. Can disable reasoning, but cannot
                enable reasoning when the configured model does not support it.
            default_reasoning_effort (Union[None, Unset, str]): Project default reasoning effort.
            supported_reasoning_efforts (Union[Unset, list[str]]): Project subset of configured-model reasoning efforts. If
                this excludes the inherited default_reasoning_effort, set default_reasoning_effort on the grant too.
            input_modalities (Union[Unset, list[str]]): Project subset of configured-model input types.
            output_modalities (Union[Unset, list[str]]): Project subset of configured-model output types.
    """

    context_window_tokens: Union[None, Unset, int] = UNSET
    max_output_tokens: Union[None, Unset, int] = UNSET
    default_max_output_tokens: Union[None, Unset, int] = UNSET
    default_cache_retention: Union[ModelCacheRetention, None, Unset] = UNSET
    supports_tools: Union[None, Unset, bool] = UNSET
    supports_reasoning: Union[None, Unset, bool] = UNSET
    default_reasoning_effort: Union[None, Unset, str] = UNSET
    supported_reasoning_efforts: Union[Unset, list[str]] = UNSET
    input_modalities: Union[Unset, list[str]] = UNSET
    output_modalities: Union[Unset, list[str]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        context_window_tokens: Union[None, Unset, int]
        if isinstance(self.context_window_tokens, Unset):
            context_window_tokens = UNSET
        else:
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

        default_cache_retention: Union[None, Unset, str]
        if isinstance(self.default_cache_retention, Unset):
            default_cache_retention = UNSET
        elif isinstance(self.default_cache_retention, str):
            default_cache_retention = self.default_cache_retention
        else:
            default_cache_retention = self.default_cache_retention

        supports_tools: Union[None, Unset, bool]
        if isinstance(self.supports_tools, Unset):
            supports_tools = UNSET
        else:
            supports_tools = self.supports_tools

        supports_reasoning: Union[None, Unset, bool]
        if isinstance(self.supports_reasoning, Unset):
            supports_reasoning = UNSET
        else:
            supports_reasoning = self.supports_reasoning

        default_reasoning_effort: Union[None, Unset, str]
        if isinstance(self.default_reasoning_effort, Unset):
            default_reasoning_effort = UNSET
        else:
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

        field_dict.update({})
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

        def _parse_context_window_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        context_window_tokens = _parse_context_window_tokens(
            d.pop("context_window_tokens", UNSET)
        )

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

        def _parse_default_cache_retention(
            data: object,
        ) -> Union[ModelCacheRetention, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                default_cache_retention_type_0 = check_model_cache_retention(data)

                return default_cache_retention_type_0
            except:  # noqa: E722
                pass
            return cast(Union[ModelCacheRetention, None, Unset], data)

        default_cache_retention = _parse_default_cache_retention(
            d.pop("default_cache_retention", UNSET)
        )

        def _parse_supports_tools(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        supports_tools = _parse_supports_tools(d.pop("supports_tools", UNSET))

        def _parse_supports_reasoning(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        supports_reasoning = _parse_supports_reasoning(
            d.pop("supports_reasoning", UNSET)
        )

        def _parse_default_reasoning_effort(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_reasoning_effort = _parse_default_reasoning_effort(
            d.pop("default_reasoning_effort", UNSET)
        )

        supported_reasoning_efforts = cast(
            list[str], d.pop("supported_reasoning_efforts", UNSET)
        )

        input_modalities = cast(list[str], d.pop("input_modalities", UNSET))

        output_modalities = cast(list[str], d.pop("output_modalities", UNSET))

        update_project_model_grant_request = cls(
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

        return update_project_model_grant_request
