from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CurrentUserIdentity")


@_attrs_define
class CurrentUserIdentity:
    """
    Attributes:
        id (str):
        email (str): The user's primary verified email, or an empty string if none.
        display_name (str):
    """

    id: str
    email: str
    display_name: str

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        email = self.email

        display_name = self.display_name

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "email": email,
                "display_name": display_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        email = d.pop("email")

        display_name = d.pop("display_name")

        current_user_identity = cls(
            id=id,
            email=email,
            display_name=display_name,
        )

        return current_user_identity
