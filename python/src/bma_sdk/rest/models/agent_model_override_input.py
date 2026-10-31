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
    """

    model: str
    provider: Union[Unset, "AgentModelOverrideProvider"] = UNSET
    api_key: Union[Unset, str] = UNSET
    ttl_seconds: Union[Unset, int] = 3600
    expires_with_session: Union[Unset, bool] = False

    def to_dict(self) -> dict[str, Any]:
        model = self.model

        provider: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider.to_dict()

        api_key = self.api_key

        ttl_seconds = self.ttl_seconds

        expires_with_session = self.expires_with_session

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

        agent_model_override_input = cls(
            model=model,
            provider=provider,
            api_key=api_key,
            ttl_seconds=ttl_seconds,
            expires_with_session=expires_with_session,
        )

        return agent_model_override_input
