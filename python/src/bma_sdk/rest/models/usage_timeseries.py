import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.usage_timeseries_group_by import (
    UsageTimeseriesGroupBy,
    check_usage_timeseries_group_by,
)
from ..models.usage_timeseries_interval import (
    UsageTimeseriesInterval,
    check_usage_timeseries_interval,
)
from ..models.usage_timeseries_metric import (
    UsageTimeseriesMetric,
    check_usage_timeseries_metric,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.usage_timeseries_series import UsageTimeseriesSeries
    from ..models.usage_totals import UsageTotals


T = TypeVar("T", bound="UsageTimeseries")


@_attrs_define
class UsageTimeseries:
    """
    Attributes:
        metric (UsageTimeseriesMetric): `sum_tokens` is input plus output tokens. `sum_cost` is provider-reported cost
            in USD. `count_model_calls` counts model calls that recorded usage.
        interval (UsageTimeseriesInterval):
        timezone (str): IANA time zone the buckets follow.
        bucket_starts (list[datetime.datetime]): Start of each bucket in `timezone`, oldest first, including buckets
            without usage. The first bucket starts at the beginning of the interval containing `since`, but only usage at or
            after `since` counts.
        until (datetime.datetime):
        totals (UsageTotals):
        active_agents (int): Agents, not counting subagents, that made at least one model call in the window.
        series (list['UsageTimeseriesSeries']): Without `group_by`, a single `all` series. With it, one series per
            ranked group, most first, then an `other` series when usage remains.
        group_by (Union[Unset, UsageTimeseriesGroupBy]):
    """

    metric: UsageTimeseriesMetric
    interval: UsageTimeseriesInterval
    timezone: str
    bucket_starts: list[datetime.datetime]
    until: datetime.datetime
    totals: "UsageTotals"
    active_agents: int
    series: list["UsageTimeseriesSeries"]
    group_by: Union[Unset, UsageTimeseriesGroupBy] = UNSET

    def to_dict(self) -> dict[str, Any]:
        metric: str = self.metric

        interval: str = self.interval

        timezone = self.timezone

        bucket_starts = []
        for bucket_starts_item_data in self.bucket_starts:
            bucket_starts_item = bucket_starts_item_data.isoformat()
            bucket_starts.append(bucket_starts_item)

        until = self.until.isoformat()

        totals = self.totals.to_dict()

        active_agents = self.active_agents

        series = []
        for series_item_data in self.series:
            series_item = series_item_data.to_dict()
            series.append(series_item)

        group_by: Union[Unset, str] = UNSET
        if not isinstance(self.group_by, Unset):
            group_by = self.group_by

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "metric": metric,
                "interval": interval,
                "timezone": timezone,
                "bucket_starts": bucket_starts,
                "until": until,
                "totals": totals,
                "active_agents": active_agents,
                "series": series,
            }
        )
        if group_by is not UNSET:
            field_dict["group_by"] = group_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_timeseries_series import UsageTimeseriesSeries
        from ..models.usage_totals import UsageTotals

        d = dict(src_dict)
        metric = check_usage_timeseries_metric(d.pop("metric"))

        interval = check_usage_timeseries_interval(d.pop("interval"))

        timezone = d.pop("timezone")

        bucket_starts = []
        _bucket_starts = d.pop("bucket_starts")
        for bucket_starts_item_data in _bucket_starts:
            bucket_starts_item = isoparse(bucket_starts_item_data)

            bucket_starts.append(bucket_starts_item)

        until = isoparse(d.pop("until"))

        totals = UsageTotals.from_dict(d.pop("totals"))

        active_agents = d.pop("active_agents")

        series = []
        _series = d.pop("series")
        for series_item_data in _series:
            series_item = UsageTimeseriesSeries.from_dict(series_item_data)

            series.append(series_item)

        _group_by = d.pop("group_by", UNSET)
        group_by: Union[Unset, UsageTimeseriesGroupBy]
        if isinstance(_group_by, Unset):
            group_by = UNSET
        else:
            group_by = check_usage_timeseries_group_by(_group_by)

        usage_timeseries = cls(
            metric=metric,
            interval=interval,
            timezone=timezone,
            bucket_starts=bucket_starts,
            until=until,
            totals=totals,
            active_agents=active_agents,
            series=series,
            group_by=group_by,
        )

        return usage_timeseries
