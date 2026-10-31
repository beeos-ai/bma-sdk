from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.current_user_identity import CurrentUserIdentity
    from ..models.current_user_org import CurrentUserOrg


T = TypeVar("T", bound="CurrentUser")


@_attrs_define
class CurrentUser:
    """
    Attributes:
        user (CurrentUserIdentity):
        orgs (list['CurrentUserOrg']):
    """

    user: "CurrentUserIdentity"
    orgs: list["CurrentUserOrg"]

    def to_dict(self) -> dict[str, Any]:
        user = self.user.to_dict()

        orgs = []
        for orgs_item_data in self.orgs:
            orgs_item = orgs_item_data.to_dict()
            orgs.append(orgs_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "user": user,
                "orgs": orgs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.current_user_identity import CurrentUserIdentity
        from ..models.current_user_org import CurrentUserOrg

        d = dict(src_dict)
        user = CurrentUserIdentity.from_dict(d.pop("user"))

        orgs = []
        _orgs = d.pop("orgs")
        for orgs_item_data in _orgs:
            orgs_item = CurrentUserOrg.from_dict(orgs_item_data)

            orgs.append(orgs_item)

        current_user = cls(
            user=user,
            orgs=orgs,
        )

        return current_user
