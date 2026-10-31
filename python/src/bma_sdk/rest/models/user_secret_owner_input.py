from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.user_secret_owner_input_kind import (
    UserSecretOwnerInputKind,
    check_user_secret_owner_input_kind,
)

T = TypeVar("T", bound="UserSecretOwnerInput")


@_attrs_define
class UserSecretOwnerInput:
    """
    Attributes:
        kind (UserSecretOwnerInputKind):
    """

    kind: UserSecretOwnerInputKind

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
        kind = check_user_secret_owner_input_kind(d.pop("kind"))

        user_secret_owner_input = cls(
            kind=kind,
        )

        return user_secret_owner_input
