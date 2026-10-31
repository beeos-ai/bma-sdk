from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.user_secret_owner_kind import (
    UserSecretOwnerKind,
    check_user_secret_owner_kind,
)

T = TypeVar("T", bound="UserSecretOwner")


@_attrs_define
class UserSecretOwner:
    """
    Attributes:
        kind (UserSecretOwnerKind):
        user_id (str):
    """

    kind: UserSecretOwnerKind
    user_id: str

    def to_dict(self) -> dict[str, Any]:
        kind: str = self.kind

        user_id = self.user_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "kind": kind,
                "user_id": user_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = check_user_secret_owner_kind(d.pop("kind"))

        user_id = d.pop("user_id")

        user_secret_owner = cls(
            kind=kind,
            user_id=user_id,
        )

        return user_secret_owner
