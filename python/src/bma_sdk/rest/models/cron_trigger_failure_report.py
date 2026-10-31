import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="CronTriggerFailureReport")


@_attrs_define
class CronTriggerFailureReport:
    """
    Attributes:
        message (str): Why the most recent failed firing did not deliver a message.
        will_retry (bool): Whether the firing will be retried after the claim lease expires.
        failed_at (datetime.datetime):
    """

    message: str
    will_retry: bool
    failed_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        will_retry = self.will_retry

        failed_at = self.failed_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "message": message,
                "will_retry": will_retry,
                "failed_at": failed_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        will_retry = d.pop("will_retry")

        failed_at = isoparse(d.pop("failed_at"))

        cron_trigger_failure_report = cls(
            message=message,
            will_retry=will_retry,
            failed_at=failed_at,
        )

        return cron_trigger_failure_report
