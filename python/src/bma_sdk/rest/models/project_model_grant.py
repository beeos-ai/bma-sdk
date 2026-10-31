import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.model_cache_retention import (
    ModelCacheRetention,
    check_model_cache_retention,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectModelGrant")


@_attrs_define
class ProjectModelGrant:
    """
    Attributes:
        id (str):
        org_id (str):
        project_id (str): Project ID (proj_...).
        configured_model_id (str):
        supported_reasoning_efforts (list[str]): Project subset of configured-model reasoning efforts. Empty means
            inherit. When non-empty, default_reasoning_effort must resolve to one of these values.
        input_modalities (list[str]): Project subset of configured-model input types (text, image, or file). Empty means
            inherit.
        output_modalities (list[str]): Project subset of configured-model output types. Empty means inherit.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        context_window_tokens (Union[None, Unset, int]): Project context budget for input and output tokens, or
            omitted/null to inherit from the configured model. Triggers compaction when estimated input exceeds the
            remaining budget after output and safety reserves. The turn fails if compaction cannot make it fit.
        max_output_tokens (Union[None, Unset, int]): Project output-token ceiling, or omitted/null to inherit from the
            configured model.
        default_max_output_tokens (Union[None, Unset, int]): Project default per-request output-token cap, or
            omitted/null to inherit from the configured model.
        default_cache_retention (Union[Unset, ModelCacheRetention]): Prompt-cache preference for model requests; `short`
            when omitted. `short` applies the route's default caching (explicit cache breakpoints where the provider
            requires them) and, where the route accepts one, a stable conversation key for cache-aware routing. `long`
            prefers the route's extended cache lifetime where one exists (currently Anthropic's one-hour cache, which on
            Bedrock requires Claude 4.5 or newer) and behaves like `short` elsewhere. `none` sends no BMA-managed cache
            controls or conversation key; providers may still cache prefixes on their own.
        supports_tools (Union[None, Unset, bool]): Project-level tool-use override, or omitted/null to inherit from the
            configured model.
        supports_reasoning (Union[None, Unset, bool]): Project-level reasoning override, or omitted/null to inherit from
            the configured model.
        default_reasoning_effort (Union[Unset, str]): Project default reasoning effort, or omitted/empty to inherit from
            the configured model.
    """

    id: str
    org_id: str
    project_id: str
    configured_model_id: str
    supported_reasoning_efforts: list[str]
    input_modalities: list[str]
    output_modalities: list[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    context_window_tokens: Union[None, Unset, int] = UNSET
    max_output_tokens: Union[None, Unset, int] = UNSET
    default_max_output_tokens: Union[None, Unset, int] = UNSET
    default_cache_retention: Union[Unset, ModelCacheRetention] = UNSET
    supports_tools: Union[None, Unset, bool] = UNSET
    supports_reasoning: Union[None, Unset, bool] = UNSET
    default_reasoning_effort: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        configured_model_id = self.configured_model_id

        supported_reasoning_efforts = self.supported_reasoning_efforts

        input_modalities = self.input_modalities

        output_modalities = self.output_modalities

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

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

        default_cache_retention: Union[Unset, str] = UNSET
        if not isinstance(self.default_cache_retention, Unset):
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

        default_reasoning_effort = self.default_reasoning_effort

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "configured_model_id": configured_model_id,
                "supported_reasoning_efforts": supported_reasoning_efforts,
                "input_modalities": input_modalities,
                "output_modalities": output_modalities,
                "created_at": created_at,
                "updated_at": updated_at,
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        configured_model_id = d.pop("configured_model_id")

        supported_reasoning_efforts = cast(
            list[str], d.pop("supported_reasoning_efforts")
        )

        input_modalities = cast(list[str], d.pop("input_modalities"))

        output_modalities = cast(list[str], d.pop("output_modalities"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

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

        _default_cache_retention = d.pop("default_cache_retention", UNSET)
        default_cache_retention: Union[Unset, ModelCacheRetention]
        if isinstance(_default_cache_retention, Unset):
            default_cache_retention = UNSET
        else:
            default_cache_retention = check_model_cache_retention(
                _default_cache_retention
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

        default_reasoning_effort = d.pop("default_reasoning_effort", UNSET)

        project_model_grant = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            configured_model_id=configured_model_id,
            supported_reasoning_efforts=supported_reasoning_efforts,
            input_modalities=input_modalities,
            output_modalities=output_modalities,
            created_at=created_at,
            updated_at=updated_at,
            context_window_tokens=context_window_tokens,
            max_output_tokens=max_output_tokens,
            default_max_output_tokens=default_max_output_tokens,
            default_cache_retention=default_cache_retention,
            supports_tools=supports_tools,
            supports_reasoning=supports_reasoning,
            default_reasoning_effort=default_reasoning_effort,
        )

        return project_model_grant
