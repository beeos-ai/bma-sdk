from typing import Literal, cast

UsageTimeseriesGroupBy = Literal["model", "profile"]

USAGE_TIMESERIES_GROUP_BY_VALUES: set[UsageTimeseriesGroupBy] = {
    "model",
    "profile",
}


def check_usage_timeseries_group_by(value: str) -> UsageTimeseriesGroupBy:
    if value in USAGE_TIMESERIES_GROUP_BY_VALUES:
        return cast(UsageTimeseriesGroupBy, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {USAGE_TIMESERIES_GROUP_BY_VALUES!r}"
    )
