from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="DesktopControlLeaseRequest")


@_attrs_define
class DesktopControlLeaseRequest:
    """
    Attributes:
        lease_seconds (Union[Unset, int]):
    """

    lease_seconds: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        lease_seconds = self.lease_seconds

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if lease_seconds is not UNSET:
            field_dict["lease_seconds"] = lease_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        lease_seconds = d.pop("lease_seconds", UNSET)

        desktop_control_lease_request = cls(
            lease_seconds=lease_seconds,
        )

        return desktop_control_lease_request
