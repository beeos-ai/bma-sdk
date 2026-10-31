from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.org_secret_owner_kind import (
    OrgSecretOwnerKind,
    check_org_secret_owner_kind,
)

T = TypeVar("T", bound="OrgSecretOwner")


@_attrs_define
class OrgSecretOwner:
    """
    Attributes:
        kind (OrgSecretOwnerKind):
    """

    kind: OrgSecretOwnerKind

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
        kind = check_org_secret_owner_kind(d.pop("kind"))

        org_secret_owner = cls(
            kind=kind,
        )

        return org_secret_owner
