from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.model_usage_totals import ModelUsageTotals
    from ..models.usage_totals import UsageTotals


T = TypeVar("T", bound="UsageReport")


@_attrs_define
class UsageReport:
    """
    Attributes:
        totals (UsageTotals):
        by_model (list['ModelUsageTotals']): Per-model rows ordered by provider config name, configured model name, then
            provider model slug. Models with distinct provider slugs across revisions appear once per slug.
    """

    totals: "UsageTotals"
    by_model: list["ModelUsageTotals"]

    def to_dict(self) -> dict[str, Any]:
        totals = self.totals.to_dict()

        by_model = []
        for by_model_item_data in self.by_model:
            by_model_item = by_model_item_data.to_dict()
            by_model.append(by_model_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "totals": totals,
                "by_model": by_model,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_usage_totals import ModelUsageTotals
        from ..models.usage_totals import UsageTotals

        d = dict(src_dict)
        totals = UsageTotals.from_dict(d.pop("totals"))

        by_model = []
        _by_model = d.pop("by_model")
        for by_model_item_data in _by_model:
            by_model_item = ModelUsageTotals.from_dict(by_model_item_data)

            by_model.append(by_model_item)

        usage_report = cls(
            totals=totals,
            by_model=by_model,
        )

        return usage_report
