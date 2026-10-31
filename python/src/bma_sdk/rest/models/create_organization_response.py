from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.organization import Organization
    from ..models.organization_membership import OrganizationMembership
    from ..models.project_fields import ProjectFields


T = TypeVar("T", bound="CreateOrganizationResponse")


@_attrs_define
class CreateOrganizationResponse:
    """
    Attributes:
        org (Organization):
        project (ProjectFields): Shared project fields composed into project response schemas. Composing schemas close
            their final shape with unevaluatedProperties.
        membership (OrganizationMembership):
    """

    org: "Organization"
    project: "ProjectFields"
    membership: "OrganizationMembership"

    def to_dict(self) -> dict[str, Any]:
        org = self.org.to_dict()

        project = self.project.to_dict()

        membership = self.membership.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "org": org,
                "project": project,
                "membership": membership,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.organization import Organization
        from ..models.organization_membership import OrganizationMembership
        from ..models.project_fields import ProjectFields

        d = dict(src_dict)
        org = Organization.from_dict(d.pop("org"))

        project = ProjectFields.from_dict(d.pop("project"))

        membership = OrganizationMembership.from_dict(d.pop("membership"))

        create_organization_response = cls(
            org=org,
            project=project,
            membership=membership,
        )

        return create_organization_response
