import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="MCPOAuthStartResponse")


@_attrs_define
class MCPOAuthStartResponse:
    """
    Attributes:
        flow_id (str):
        authorization_url (str):
        expires_at (datetime.datetime):
    """

    flow_id: str
    authorization_url: str
    expires_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        flow_id = self.flow_id

        authorization_url = self.authorization_url

        expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "flow_id": flow_id,
                "authorization_url": authorization_url,
                "expires_at": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        flow_id = d.pop("flow_id")

        authorization_url = d.pop("authorization_url")

        expires_at = isoparse(d.pop("expires_at"))

        mcpo_auth_start_response = cls(
            flow_id=flow_id,
            authorization_url=authorization_url,
            expires_at=expires_at,
        )

        return mcpo_auth_start_response
