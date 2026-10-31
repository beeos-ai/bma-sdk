from typing import Literal, cast

UsageTimeseriesMetric = Literal[
    "count_model_calls",
    "sum_cost",
    "sum_input_tokens",
    "sum_output_tokens",
    "sum_tokens",
]

USAGE_TIMESERIES_METRIC_VALUES: set[UsageTimeseriesMetric] = {
    "count_model_calls",
    "sum_cost",
    "sum_input_tokens",
    "sum_output_tokens",
    "sum_tokens",
}


def check_usage_timeseries_metric(value: str) -> UsageTimeseriesMetric:
    if value in USAGE_TIMESERIES_METRIC_VALUES:
        return cast(UsageTimeseriesMetric, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {USAGE_TIMESERIES_METRIC_VALUES!r}"
    )
