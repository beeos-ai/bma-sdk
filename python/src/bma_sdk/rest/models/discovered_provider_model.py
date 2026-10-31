from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.discovered_model_pricing import DiscoveredModelPricing


T = TypeVar("T", bound="DiscoveredProviderModel")


@_attrs_define
class DiscoveredProviderModel:
    """
    Attributes:
        slug (str): Provider model slug usable as a configured model's provider_model_slug.
        display_name (Union[Unset, str]):
        context_window_tokens (Union[Unset, int]): Provider-advertised context window limit in tokens, when available.
        max_output_tokens (Union[Unset, int]): Provider-advertised maximum output limit in tokens, when available.
        supports_reasoning (Union[Unset, bool]): Whether BMA can send this model a reasoning effort, when the provider
            or the public model catalog reports it.
        supported_reasoning_efforts (Union[Unset, list[str]]): Reasoning effort values the model accepts, when reported.
        pricing (Union[Unset, DiscoveredModelPricing]): Provider-advertised list prices in USD per million tokens, as
            exact decimal strings. Present only when the provider publishes pricing in its model catalog (OpenRouter). Cache
            prices are omitted when the provider does not publish them.
    """

    slug: str
    display_name: Union[Unset, str] = UNSET
    context_window_tokens: Union[Unset, int] = UNSET
    max_output_tokens: Union[Unset, int] = UNSET
    supports_reasoning: Union[Unset, bool] = UNSET
    supported_reasoning_efforts: Union[Unset, list[str]] = UNSET
    pricing: Union[Unset, "DiscoveredModelPricing"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        slug = self.slug

        display_name = self.display_name

        context_window_tokens = self.context_window_tokens

        max_output_tokens = self.max_output_tokens

        supports_reasoning = self.supports_reasoning

        supported_reasoning_efforts: Union[Unset, list[str]] = UNSET
        if not isinstance(self.supported_reasoning_efforts, Unset):
            supported_reasoning_efforts = self.supported_reasoning_efforts

        pricing: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.pricing, Unset):
            pricing = self.pricing.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "slug": slug,
            }
        )
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if context_window_tokens is not UNSET:
            field_dict["context_window_tokens"] = context_window_tokens
        if max_output_tokens is not UNSET:
            field_dict["max_output_tokens"] = max_output_tokens
        if supports_reasoning is not UNSET:
            field_dict["supports_reasoning"] = supports_reasoning
        if supported_reasoning_efforts is not UNSET:
            field_dict["supported_reasoning_efforts"] = supported_reasoning_efforts
        if pricing is not UNSET:
            field_dict["pricing"] = pricing

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.discovered_model_pricing import DiscoveredModelPricing

        d = dict(src_dict)
        slug = d.pop("slug")

        display_name = d.pop("display_name", UNSET)

        context_window_tokens = d.pop("context_window_tokens", UNSET)

        max_output_tokens = d.pop("max_output_tokens", UNSET)

        supports_reasoning = d.pop("supports_reasoning", UNSET)

        supported_reasoning_efforts = cast(
            list[str], d.pop("supported_reasoning_efforts", UNSET)
        )

        _pricing = d.pop("pricing", UNSET)
        pricing: Union[Unset, DiscoveredModelPricing]
        if isinstance(_pricing, Unset):
            pricing = UNSET
        else:
            pricing = DiscoveredModelPricing.from_dict(_pricing)

        discovered_provider_model = cls(
            slug=slug,
            display_name=display_name,
            context_window_tokens=context_window_tokens,
            max_output_tokens=max_output_tokens,
            supports_reasoning=supports_reasoning,
            supported_reasoning_efforts=supported_reasoning_efforts,
            pricing=pricing,
        )

        return discovered_provider_model
