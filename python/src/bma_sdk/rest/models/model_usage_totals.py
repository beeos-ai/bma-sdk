from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.model_usage_totals_purpose import (
    ModelUsageTotalsPurpose,
    check_model_usage_totals_purpose,
)
from ..types import UNSET, Unset

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
        purpose (Union[Unset, ModelUsageTotalsPurpose]): What the calls were for. `turn` is ordinary agent model calls;
            `title` is the automatic session-title request, made with the session's own model credentials; `harness` is the
            model requests of an ACP harness (agent config `harness.kind: acp`) through the platform's harness model
            endpoint. A model used for several appears once per purpose.
    """

    model: "UsageModel"
    model_calls: int
    tokens: "UsageTokenTotals"
    cost: "UsageCostTotals"
    purpose: Union[Unset, ModelUsageTotalsPurpose] = UNSET

    def to_dict(self) -> dict[str, Any]:
        model = self.model.to_dict()

        model_calls = self.model_calls

        tokens = self.tokens.to_dict()

        cost = self.cost.to_dict()

        purpose: Union[Unset, str] = UNSET
        if not isinstance(self.purpose, Unset):
            purpose = self.purpose

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "model": model,
                "model_calls": model_calls,
                "tokens": tokens,
                "cost": cost,
            }
        )
        if purpose is not UNSET:
            field_dict["purpose"] = purpose

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

        _purpose = d.pop("purpose", UNSET)
        purpose: Union[Unset, ModelUsageTotalsPurpose]
        if isinstance(_purpose, Unset):
            purpose = UNSET
        else:
            purpose = check_model_usage_totals_purpose(_purpose)

        model_usage_totals = cls(
            model=model,
            model_calls=model_calls,
            tokens=tokens,
            cost=cost,
            purpose=purpose,
        )

        return model_usage_totals
