from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.configured_model_summary import ConfiguredModelSummary
    from ..models.project_model_grant import ProjectModelGrant
    from ..models.project_model_grant_effective_reasoning import (
        ProjectModelGrantEffectiveReasoning,
    )


T = TypeVar("T", bound="ProjectModelGrantListItem")


@_attrs_define
class ProjectModelGrantListItem:
    """
    Attributes:
        grant (ProjectModelGrant):
        model (ConfiguredModelSummary):
        effective_reasoning (ProjectModelGrantEffectiveReasoning): Reasoning settings agents in this project get for the
            model, after project grant overrides are applied to the configured model's current revision.
    """

    grant: "ProjectModelGrant"
    model: "ConfiguredModelSummary"
    effective_reasoning: "ProjectModelGrantEffectiveReasoning"

    def to_dict(self) -> dict[str, Any]:
        grant = self.grant.to_dict()

        model = self.model.to_dict()

        effective_reasoning = self.effective_reasoning.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "grant": grant,
                "model": model,
                "effective_reasoning": effective_reasoning,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.configured_model_summary import ConfiguredModelSummary
        from ..models.project_model_grant import ProjectModelGrant
        from ..models.project_model_grant_effective_reasoning import (
            ProjectModelGrantEffectiveReasoning,
        )

        d = dict(src_dict)
        grant = ProjectModelGrant.from_dict(d.pop("grant"))

        model = ConfiguredModelSummary.from_dict(d.pop("model"))

        effective_reasoning = ProjectModelGrantEffectiveReasoning.from_dict(
            d.pop("effective_reasoning")
        )

        project_model_grant_list_item = cls(
            grant=grant,
            model=model,
            effective_reasoning=effective_reasoning,
        )

        return project_model_grant_list_item
