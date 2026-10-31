from typing import Literal, cast

UsageTimeseriesInterval = Literal["day", "hour", "month", "week"]

USAGE_TIMESERIES_INTERVAL_VALUES: set[UsageTimeseriesInterval] = {
    "day",
    "hour",
    "month",
    "week",
}


def check_usage_timeseries_interval(value: str) -> UsageTimeseriesInterval:
    if value in USAGE_TIMESERIES_INTERVAL_VALUES:
        return cast(UsageTimeseriesInterval, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {USAGE_TIMESERIES_INTERVAL_VALUES!r}"
    )
