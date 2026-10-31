import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.cron_trigger_last_run_state import (
    CronTriggerLastRunState,
    check_cron_trigger_last_run_state,
)

T = TypeVar("T", bound="CronTriggerLastRun")


@_attrs_define
class CronTriggerLastRun:
    """
    Attributes:
        state (CronTriggerLastRunState): State of the latest accepted scheduled integration action. Completed means the
            integration handled the occurrence; it does not indicate completion of any agent task that action started.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        failure_message (Union[None, str]): Coarse scheduled action failure description; no raw provider errors.
    """

    state: CronTriggerLastRunState
    created_at: datetime.datetime
    updated_at: datetime.datetime
    failure_message: Union[None, str]

    def to_dict(self) -> dict[str, Any]:
        state: str = self.state

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        failure_message: Union[None, str]
        failure_message = self.failure_message

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "state": state,
                "created_at": created_at,
                "updated_at": updated_at,
                "failure_message": failure_message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        state = check_cron_trigger_last_run_state(d.pop("state"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_failure_message(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        failure_message = _parse_failure_message(d.pop("failure_message"))

        cron_trigger_last_run = cls(
            state=state,
            created_at=created_at,
            updated_at=updated_at,
            failure_message=failure_message,
        )

        return cron_trigger_last_run
