from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ProjectAccess")


@_attrs_define
class ProjectAccess:
    """
    Attributes:
        can_read (bool):
        can_manage (bool):
        can_manage_access (bool):
        can_operate (bool):
    """

    can_read: bool
    can_manage: bool
    can_manage_access: bool
    can_operate: bool

    def to_dict(self) -> dict[str, Any]:
        can_read = self.can_read

        can_manage = self.can_manage

        can_manage_access = self.can_manage_access

        can_operate = self.can_operate

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "can_read": can_read,
                "can_manage": can_manage,
                "can_manage_access": can_manage_access,
                "can_operate": can_operate,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        can_read = d.pop("can_read")

        can_manage = d.pop("can_manage")

        can_manage_access = d.pop("can_manage_access")

        can_operate = d.pop("can_operate")

        project_access = cls(
            can_read=can_read,
            can_manage=can_manage,
            can_manage_access=can_manage_access,
            can_operate=can_operate,
        )

        return project_access
