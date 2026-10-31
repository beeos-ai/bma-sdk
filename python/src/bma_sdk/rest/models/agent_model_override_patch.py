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


T = TypeVar("T", bound="AgentModelOverridePatch")


@_attrs_define
class AgentModelOverridePatch:
    """
    Attributes:
        model (Union[Unset, str]):
        provider (Union[Unset, AgentModelOverrideProvider]):
        api_key (Union[Unset, str]):
        ttl_seconds (Union[Unset, int]):
    """

    model: Union[Unset, str] = UNSET
    provider: Union[Unset, "AgentModelOverrideProvider"] = UNSET
    api_key: Union[Unset, str] = UNSET
    ttl_seconds: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        model = self.model

        provider: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.provider, Unset):
            provider = self.provider.to_dict()

        api_key = self.api_key

        ttl_seconds = self.ttl_seconds

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if model is not UNSET:
            field_dict["model"] = model
        if provider is not UNSET:
            field_dict["provider"] = provider
        if api_key is not UNSET:
            field_dict["api_key"] = api_key
        if ttl_seconds is not UNSET:
            field_dict["ttl_seconds"] = ttl_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_model_override_provider import AgentModelOverrideProvider

        d = dict(src_dict)
        model = d.pop("model", UNSET)

        _provider = d.pop("provider", UNSET)
        provider: Union[Unset, AgentModelOverrideProvider]
        if isinstance(_provider, Unset):
            provider = UNSET
        else:
            provider = AgentModelOverrideProvider.from_dict(_provider)

        api_key = d.pop("api_key", UNSET)

        ttl_seconds = d.pop("ttl_seconds", UNSET)

        agent_model_override_patch = cls(
            model=model,
            provider=provider,
            api_key=api_key,
            ttl_seconds=ttl_seconds,
        )

        return agent_model_override_patch
