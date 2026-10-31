from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..models.usage_timeseries_series_kind import (
    UsageTimeseriesSeriesKind,
    check_usage_timeseries_series_kind,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="UsageTimeseriesSeries")


@_attrs_define
class UsageTimeseriesSeries:
    """
    Attributes:
        kind (UsageTimeseriesSeriesKind): `no_profile` groups usage from agents launched without a profile; `other`
            folds together every group beyond `group_limit`.
        total (float): Metric over the whole window.
        values (list[float]): Metric in each bucket, aligned with `bucket_starts`.
        id (Union[Unset, str]): Configured model ID for `model` series, agent profile ID for `profile` series.
        name (Union[Unset, str]): Human-readable name. Spaces and punctuation are allowed; leading or trailing
            whitespace and invisible or control characters are not.
        model_provider_config_name (Union[Unset, str]): Human-readable name. Spaces and punctuation are allowed; leading
            or trailing whitespace and invisible or control characters are not.
        project_name (Union[Unset, str]): Human-readable name. Spaces and punctuation are allowed; leading or trailing
            whitespace and invisible or control characters are not.
    """

    kind: UsageTimeseriesSeriesKind
    total: float
    values: list[float]
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    model_provider_config_name: Union[Unset, str] = UNSET
    project_name: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        total = self.total

        values = self.values

        id = self.id

        name = self.name

        model_provider_config_name = self.model_provider_config_name

        project_name = self.project_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "total": total,
                "values": values,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if model_provider_config_name is not UNSET:
            field_dict["model_provider_config_name"] = model_provider_config_name
        if project_name is not UNSET:
            field_dict["project_name"] = project_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_usage_timeseries_series_kind(d.pop("kind"))

        total = d.pop("total")

        values = cast(list[float], d.pop("values"))

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        model_provider_config_name = d.pop("model_provider_config_name", UNSET)

        project_name = d.pop("project_name", UNSET)

        usage_timeseries_series = cls(
            kind=kind,
            total=total,
            values=values,
            id=id,
            name=name,
            model_provider_config_name=model_provider_config_name,
            project_name=project_name,
        )

        return usage_timeseries_series
