from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.project_model_grant import ProjectModelGrant


T = TypeVar("T", bound="ProjectModelGrantEnvelope")


@_attrs_define
class ProjectModelGrantEnvelope:
    """
    Attributes:
        grant (ProjectModelGrant):
    """

    grant: "ProjectModelGrant"

    def to_dict(self) -> dict[str, Any]:
        grant = self.grant.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "grant": grant,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_model_grant import ProjectModelGrant

        d = dict(src_dict)
        grant = ProjectModelGrant.from_dict(d.pop("grant"))

        project_model_grant_envelope = cls(
            grant=grant,
        )

        return project_model_grant_envelope
