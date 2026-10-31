from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.usage_cost_totals import UsageCostTotals
    from ..models.usage_model import UsageModel
    from ..models.usage_token_totals import UsageTokenTotals


T = TypeVar("T", bound="ModelUsageTotals")


@_attrs_define
class ModelUsageTotals:
    """
    Attributes:
        model (UsageModel):
        model_calls (int):
        tokens (UsageTokenTotals): Summed token counts across the tallied model calls. Input totals are the sum of
            uncached, cache-read, and cache-write tokens; output totals include reasoning tokens.
        cost (UsageCostTotals):
    """

    model: "UsageModel"
    model_calls: int
    tokens: "UsageTokenTotals"
    cost: "UsageCostTotals"

    def to_dict(self) -> dict[str, Any]:
        model = self.model.to_dict()

        model_calls = self.model_calls

        tokens = self.tokens.to_dict()

        cost = self.cost.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "model": model,
                "model_calls": model_calls,
                "tokens": tokens,
                "cost": cost,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_cost_totals import UsageCostTotals
        from ..models.usage_model import UsageModel
        from ..models.usage_token_totals import UsageTokenTotals

        d = dict(src_dict)
        model = UsageModel.from_dict(d.pop("model"))

        model_calls = d.pop("model_calls")

        tokens = UsageTokenTotals.from_dict(d.pop("tokens"))

        cost = UsageCostTotals.from_dict(d.pop("cost"))

        model_usage_totals = cls(
            model=model,
            model_calls=model_calls,
            tokens=tokens,
            cost=cost,
        )

        return model_usage_totals
