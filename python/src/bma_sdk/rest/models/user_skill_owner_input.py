from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.user_skill_owner_input_kind import (
    UserSkillOwnerInputKind,
    check_user_skill_owner_input_kind,
)

T = TypeVar("T", bound="UserSkillOwnerInput")


@_attrs_define
class UserSkillOwnerInput:
    """
    Attributes:
        kind (UserSkillOwnerInputKind):
    """

    kind: UserSkillOwnerInputKind

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
        kind = check_user_skill_owner_input_kind(d.pop("kind"))

        user_skill_owner_input = cls(
            kind=kind,
        )

        return user_skill_owner_input
