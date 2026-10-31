from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.project_secret_owner_kind import (
    ProjectSecretOwnerKind,
    check_project_secret_owner_kind,
)

T = TypeVar("T", bound="ProjectSecretOwner")


@_attrs_define
class ProjectSecretOwner:
    """
    Attributes:
        kind (ProjectSecretOwnerKind):
        project_id (str): Project ID (proj_...).
    """

    kind: ProjectSecretOwnerKind
    project_id: str

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        project_id = self.project_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "project_id": project_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_project_secret_owner_kind(d.pop("kind"))

        project_id = d.pop("project_id")

        project_secret_owner = cls(
            kind=kind,
            project_id=project_id,
        )

        return project_secret_owner
