from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateConnectionTicketRequest")


@_attrs_define
class CreateConnectionTicketRequest:
    """
    Attributes:
        ttl_seconds (Union[Unset, int]):
    """

    ttl_seconds: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        ttl_seconds = self.ttl_seconds

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if ttl_seconds is not UNSET:
            field_dict["ttl_seconds"] = ttl_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ttl_seconds = d.pop("ttl_seconds", UNSET)

        create_connection_ticket_request = cls(
            ttl_seconds=ttl_seconds,
        )

        return create_connection_ticket_request
