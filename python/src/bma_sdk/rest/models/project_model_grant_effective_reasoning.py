from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define

T = TypeVar("T", bound="ProjectModelGrantEffectiveReasoning")


@_attrs_define
class ProjectModelGrantEffectiveReasoning:
    """Reasoning settings agents in this project get for the model, after project grant overrides are applied to the
    configured model's current revision.

        Attributes:
            supports_reasoning (bool): Whether agents can use this model's reasoning features. False when the grant no
                longer fits the configured model.
            default_reasoning_effort (str): Reasoning effort sent when an agent config does not set model.reasoning.effort.
                Empty means the provider default.
            supported_reasoning_efforts (list[str]): Values an agent config may set as model.reasoning.effort, including
                limits the model's API format imposes when the configured model lists none. Empty means any value is accepted.
    """

    supports_reasoning: bool
    default_reasoning_effort: str
    supported_reasoning_efforts: list[str]

    def to_dict(self) -> dict[str, Any]:
        supports_reasoning = self.supports_reasoning

        default_reasoning_effort = self.default_reasoning_effort

        supported_reasoning_efforts = self.supported_reasoning_efforts

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "supports_reasoning": supports_reasoning,
                "default_reasoning_effort": default_reasoning_effort,
                "supported_reasoning_efforts": supported_reasoning_efforts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        supports_reasoning = d.pop("supports_reasoning")

        default_reasoning_effort = d.pop("default_reasoning_effort")

        supported_reasoning_efforts = cast(
            list[str], d.pop("supported_reasoning_efforts")
        )

        project_model_grant_effective_reasoning = cls(
            supports_reasoning=supports_reasoning,
            default_reasoning_effort=default_reasoning_effort,
            supported_reasoning_efforts=supported_reasoning_efforts,
        )

        return project_model_grant_effective_reasoning
