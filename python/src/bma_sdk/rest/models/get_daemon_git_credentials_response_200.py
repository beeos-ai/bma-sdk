import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="GetDaemonGitCredentialsResponse200")


@_attrs_define
class GetDaemonGitCredentialsResponse200:
    """
    Attributes:
        token (str):
        expires_at (datetime.datetime):
    """

    token: str
    expires_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        token = self.token

        expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "token": token,
                "expires_at": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        token = d.pop("token")

        expires_at = isoparse(d.pop("expires_at"))

        get_daemon_git_credentials_response_200 = cls(
            token=token,
            expires_at=expires_at,
        )

        return get_daemon_git_credentials_response_200
