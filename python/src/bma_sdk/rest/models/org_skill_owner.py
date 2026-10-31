from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.org_skill_owner_kind import OrgSkillOwnerKind, check_org_skill_owner_kind

T = TypeVar("T", bound="OrgSkillOwner")


@_attrs_define
class OrgSkillOwner:
    """
    Attributes:
        kind (OrgSkillOwnerKind):
    """

    kind: OrgSkillOwnerKind

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_org_skill_owner_kind(d.pop("kind"))

        org_skill_owner = cls(
            kind=kind,
        )

        return org_skill_owner
