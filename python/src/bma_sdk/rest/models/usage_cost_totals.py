from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="UsageCostTotals")


@_attrs_define
class UsageCostTotals:
    """
    Attributes:
        provider_reported_usd (str): Exact decimal sum in USD of the costs the provider reported for the tallied model
            calls. Calls whose provider reported no cost contribute nothing; compare model_calls_with_reported_cost against
            model_calls to see how complete the figure is.
        model_calls_with_reported_cost (int):
    """

    provider_reported_usd: str
    model_calls_with_reported_cost: int

    def to_dict(self) -> dict[str, Any]:
        provider_reported_usd = self.provider_reported_usd

        model_calls_with_reported_cost = self.model_calls_with_reported_cost

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "provider_reported_usd": provider_reported_usd,
                "model_calls_with_reported_cost": model_calls_with_reported_cost,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        provider_reported_usd = d.pop("provider_reported_usd")

        model_calls_with_reported_cost = d.pop("model_calls_with_reported_cost")

        usage_cost_totals = cls(
            provider_reported_usd=provider_reported_usd,
            model_calls_with_reported_cost=model_calls_with_reported_cost,
        )

        return usage_cost_totals
