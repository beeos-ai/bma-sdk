from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DiscoveredModelPricing")


@_attrs_define
class DiscoveredModelPricing:
    """Provider-advertised list prices in USD per million tokens, as exact decimal strings. Present only when the provider
    publishes pricing in its model catalog (OpenRouter). Cache prices are omitted when the provider does not publish
    them.

        Attributes:
            input_usd_per_million (str):
            output_usd_per_million (str):
            cache_read_input_usd_per_million (Union[Unset, str]):
            cache_write_input_usd_per_million (Union[Unset, str]):
    """

    input_usd_per_million: str
    output_usd_per_million: str
    cache_read_input_usd_per_million: Union[Unset, str] = UNSET
    cache_write_input_usd_per_million: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        input_usd_per_million = self.input_usd_per_million

        output_usd_per_million = self.output_usd_per_million

        cache_read_input_usd_per_million = self.cache_read_input_usd_per_million

        cache_write_input_usd_per_million = self.cache_write_input_usd_per_million

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "input_usd_per_million": input_usd_per_million,
                "output_usd_per_million": output_usd_per_million,
            }
        )
        if cache_read_input_usd_per_million is not UNSET:
            field_dict["cache_read_input_usd_per_million"] = (
                cache_read_input_usd_per_million
            )
        if cache_write_input_usd_per_million is not UNSET:
            field_dict["cache_write_input_usd_per_million"] = (
                cache_write_input_usd_per_million
            )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        input_usd_per_million = d.pop("input_usd_per_million")

        output_usd_per_million = d.pop("output_usd_per_million")

        cache_read_input_usd_per_million = d.pop(
            "cache_read_input_usd_per_million", UNSET
        )

        cache_write_input_usd_per_million = d.pop(
            "cache_write_input_usd_per_million", UNSET
        )

        discovered_model_pricing = cls(
            input_usd_per_million=input_usd_per_million,
            output_usd_per_million=output_usd_per_million,
            cache_read_input_usd_per_million=cache_read_input_usd_per_million,
            cache_write_input_usd_per_million=cache_write_input_usd_per_million,
        )

        return discovered_model_pricing
