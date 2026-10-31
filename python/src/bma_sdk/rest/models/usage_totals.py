from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.usage_cost_totals import UsageCostTotals
    from ..models.usage_token_totals import UsageTokenTotals


T = TypeVar("T", bound="UsageTotals")


@_attrs_define
class UsageTotals:
    """
    Attributes:
        model_calls (int): Model calls that recorded token usage or a provider-reported cost.
        tokens (UsageTokenTotals): Summed token counts across the tallied model calls. Input totals are the sum of
            uncached, cache-read, and cache-write tokens; output totals include reasoning tokens.
        cost (UsageCostTotals):
    """

    model_calls: int
    tokens: "UsageTokenTotals"
    cost: "UsageCostTotals"

    def to_dict(self) -> dict[str, Any]:
        model_calls = self.model_calls

        tokens = self.tokens.to_dict()

        cost = self.cost.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "model_calls": model_calls,
                "tokens": tokens,
                "cost": cost,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_cost_totals import UsageCostTotals
        from ..models.usage_token_totals import UsageTokenTotals

        d = dict(src_dict)
        model_calls = d.pop("model_calls")

        tokens = UsageTokenTotals.from_dict(d.pop("tokens"))

        cost = UsageCostTotals.from_dict(d.pop("cost"))

        usage_totals = cls(
            model_calls=model_calls,
            tokens=tokens,
            cost=cost,
        )

        return usage_totals
