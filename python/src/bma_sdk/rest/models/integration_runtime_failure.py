import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="IntegrationRuntimeFailure")


@_attrs_define
class IntegrationRuntimeFailure:
    """Most recent connection failure for the active integration's current setup and credential version. Returned only by
    Get integration, not list or mutation responses. Omission does not establish provider connectivity; a runtime lease
    is not a connection check.

        Attributes:
            message (str): Connection failure recorded by the integration runtime.
            retry_at (datetime.datetime):
    """

    message: str
    retry_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        retry_at = self.retry_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "message": message,
                "retry_at": retry_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        retry_at = isoparse(d.pop("retry_at"))

        integration_runtime_failure = cls(
            message=message,
            retry_at=retry_at,
        )

        return integration_runtime_failure
