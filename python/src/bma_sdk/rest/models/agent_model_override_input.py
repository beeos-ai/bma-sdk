from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_model_override_provider import AgentModelOverrideProvider


T = TypeVar("T", bound="AgentModelOverrideInput")


@_attrs_define
class AgentModelOverrideInput:
    """
    Attributes:
        model (str): Provider model slug (for example deepseek-flash).
        provider (Union[Unset, AgentModelOverrideProvider]):
        api_key (Union[Unset, str]): Write-only. Never returned, logged, or emitted; encrypted at rest.
        ttl_seconds (Union[Unset, int]):  Default: 3600.
        expires_with_session (Union[Unset, bool]): Keep the override active until the session is archived instead of a
            TTL. Default: False.
        context_window_tokens (Union[Unset, int]): Model context window in tokens. When omitted, BMA reads it from the
            provider's models endpoint, then a public model catalog, and otherwise uses 128000.
        max_output_tokens (Union[Unset, int]): Maximum output tokens per response; must be below the context window.
            When omitted, BMA keeps its default output policy for the API format.
        auto_compact_window_tokens (Union[Unset, int]): Compact the session as if the context window were this size, to
            bound per-turn cost and latency on large-window models. Must not exceed the context window.
    """

    model: str
    provider: Union[Unset, "AgentModelOverrideProvider"] = UNSET
    api_key: Union[Unset, str] = UNSET
    ttl_seconds: Union[Unset, int] = 3600
    expires_with_session: Union[Unset, bool] = False
    context_window_tokens: Union[Unset, int] = UNSET
    max_output_tokens: Union[Unset, int] = UNSET
    auto_compact_window_tokens: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        model = self.model

        provider: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider.to_dict()

        api_key = self.api_key

        ttl_seconds = self.ttl_seconds

        expires_with_session = self.expires_with_session

        context_window_tokens = self.context_window_tokens

        max_output_tokens = self.max_output_tokens

        auto_compact_window_tokens = self.auto_compact_window_tokens

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "model": model,
            }
        )
        if provider is not UNSET:
            field_dict["provider"] = provider
        if api_key is not UNSET:
            field_dict["api_key"] = api_key
        if ttl_seconds is not UNSET:
            field_dict["ttl_seconds"] = ttl_seconds
        if expires_with_session is not UNSET:
            field_dict["expires_with_session"] = expires_with_session
        if context_window_tokens is not UNSET:
            field_dict["context_window_tokens"] = context_window_tokens
        if max_output_tokens is not UNSET:
            field_dict["max_output_tokens"] = max_output_tokens
        if auto_compact_window_tokens is not UNSET:
            field_dict["auto_compact_window_tokens"] = auto_compact_window_tokens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_model_override_provider import AgentModelOverrideProvider

        d = dict(src_dict)
        model = d.pop("model")

        _provider = d.pop("provider", UNSET)
        provider: Union[Unset, AgentModelOverrideProvider]
        if isinstance(_provider, Unset):
            provider = UNSET
        else:
            provider = AgentModelOverrideProvider.from_dict(_provider)

        api_key = d.pop("api_key", UNSET)

        ttl_seconds = d.pop("ttl_seconds", UNSET)

        expires_with_session = d.pop("expires_with_session", UNSET)

        context_window_tokens = d.pop("context_window_tokens", UNSET)

        max_output_tokens = d.pop("max_output_tokens", UNSET)

        auto_compact_window_tokens = d.pop("auto_compact_window_tokens", UNSET)

        agent_model_override_input = cls(
            model=model,
            provider=provider,
            api_key=api_key,
            ttl_seconds=ttl_seconds,
            expires_with_session=expires_with_session,
            context_window_tokens=context_window_tokens,
            max_output_tokens=max_output_tokens,
            auto_compact_window_tokens=auto_compact_window_tokens,
        )

        return agent_model_override_input
