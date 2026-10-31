from typing import Literal, cast

UsageTimeseriesSeriesKind = Literal["all", "model", "no_profile", "other", "profile"]

USAGE_TIMESERIES_SERIES_KIND_VALUES: set[UsageTimeseriesSeriesKind] = {
    "all",
    "model",
    "no_profile",
    "other",
    "profile",
}


def check_usage_timeseries_series_kind(value: str) -> UsageTimeseriesSeriesKind:
    if value in USAGE_TIMESERIES_SERIES_KIND_VALUES:
        return cast(UsageTimeseriesSeriesKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {USAGE_TIMESERIES_SERIES_KIND_VALUES!r}"
    )
