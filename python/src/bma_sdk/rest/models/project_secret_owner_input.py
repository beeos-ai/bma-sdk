from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.project_secret_owner_input_kind import (
    ProjectSecretOwnerInputKind,
    check_project_secret_owner_input_kind,
)

T = TypeVar("T", bound="ProjectSecretOwnerInput")


@_attrs_define
class ProjectSecretOwnerInput:
    """
    Attributes:
        kind (ProjectSecretOwnerInputKind):
        project_id (str): Project ID (proj_...).
    """

    kind: ProjectSecretOwnerInputKind
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
        kind = check_project_secret_owner_input_kind(d.pop("kind"))

        project_id = d.pop("project_id")

        project_secret_owner_input = cls(
            kind=kind,
            project_id=project_id,
        )

        return project_secret_owner_input
