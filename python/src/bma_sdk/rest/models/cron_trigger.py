import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_cron_trigger_target import AgentCronTriggerTarget
    from ..models.agent_profile_cron_trigger_target import AgentProfileCronTriggerTarget
    from ..models.cron_trigger_failure_report import CronTriggerFailureReport
    from ..models.cron_trigger_last_run import CronTriggerLastRun
    from ..models.integration_cron_trigger_target import IntegrationCronTriggerTarget


T = TypeVar("T", bound="CronTrigger")


@_attrs_define
class CronTrigger:
    """
    Attributes:
        id (str):
        org_id (str):
        project_id (str): Project ID (proj_...).
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        target (Union['AgentCronTriggerTarget', 'AgentProfileCronTriggerTarget', 'IntegrationCronTriggerTarget']): What
            each firing does: type agent sends the message to an existing agent, type profile launches a new agent from a
            profile, and type integration hands the firing to an integration, such as a new Slack or Discord thread.
        cron (str): Standard five-field cron expression (minute, hour, day of month, month, day of week).
            `TZ=`/`CRON_TZ=` prefixes are rejected; set the `timezone` field instead.
        timezone (str): IANA time zone the schedule is evaluated in.
        enabled (bool):
        last_fired_at (Union[None, datetime.datetime]): When the trigger last fired, or null if it has never fired. For
            integration targets this means durable inbox handoff.
        next_fire_at (Union[None, datetime.datetime]): Next scheduled firing, or null while the trigger is disabled.
        failure_report (Union['CronTriggerFailureReport', None]): Most recent failed firing, or null if no firing has
            failed since the last successful firing.
        last_run (Union['CronTriggerLastRun', None]): Status of the latest accepted scheduled integration launch, scoped
            to this project and integration. Null for ordinary cron, before any launch is accepted, or when retained details
            have expired. Never falls back to an older launch. Schedule firing failures remain separate in failure_report.
            Deleting or disabling a schedule does not cancel launch work already accepted by the integration.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        message_template (Union[Unset, str]): Go text/template rendered on each firing to produce the message sent to
            the target. The template receives a `trigger` value with `name`, `fired_at`, `last_fired_at`, and `local_date`
            fields. Timestamps remain UTC; local_date is the scheduled occurrence's ISO date in the schedule timezone.
            Required for agent and profile targets; omitted for integration targets, which use their own settings. Rendering
            is capped at 64 KiB of output and one second of wall-clock time, and `printf` width and precision specifiers are
            capped at 1024; a firing whose template fails to render is recorded in `failure_report` without sending a
            message.
    """

    id: str
    org_id: str
    project_id: str
    name: str
    target: Union[
        "AgentCronTriggerTarget",
        "AgentProfileCronTriggerTarget",
        "IntegrationCronTriggerTarget",
    ]
    cron: str
    timezone: str
    enabled: bool
    last_fired_at: Union[None, datetime.datetime]
    next_fire_at: Union[None, datetime.datetime]
    failure_report: Union["CronTriggerFailureReport", None]
    last_run: Union["CronTriggerLastRun", None]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    message_template: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_cron_trigger_target import AgentCronTriggerTarget
        from ..models.agent_profile_cron_trigger_target import (
            AgentProfileCronTriggerTarget,
        )
        from ..models.cron_trigger_failure_report import CronTriggerFailureReport
        from ..models.cron_trigger_last_run import CronTriggerLastRun

        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        name = self.name

        target: dict[str, Any]
        if isinstance(self.target, AgentCronTriggerTarget):
            target = self.target.to_dict()
        elif isinstance(self.target, AgentProfileCronTriggerTarget):
            target = self.target.to_dict()
        else:
            target = self.target.to_dict()

        cron = self.cron

        timezone = self.timezone

        enabled = self.enabled

        last_fired_at: Union[None, str]
        if isinstance(self.last_fired_at, datetime.datetime):
            last_fired_at = self.last_fired_at.isoformat()
        else:
            last_fired_at = self.last_fired_at

        next_fire_at: Union[None, str]
        if isinstance(self.next_fire_at, datetime.datetime):
            next_fire_at = self.next_fire_at.isoformat()
        else:
            next_fire_at = self.next_fire_at

        failure_report: Union[None, dict[str, Any]]
        if isinstance(self.failure_report, CronTriggerFailureReport):
            failure_report = self.failure_report.to_dict()
        else:
            failure_report = self.failure_report

        last_run: Union[None, dict[str, Any]]
        if isinstance(self.last_run, CronTriggerLastRun):
            last_run = self.last_run.to_dict()
        else:
            last_run = self.last_run

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        message_template = self.message_template

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "name": name,
                "target": target,
                "cron": cron,
                "timezone": timezone,
                "enabled": enabled,
                "last_fired_at": last_fired_at,
                "next_fire_at": next_fire_at,
                "failure_report": failure_report,
                "last_run": last_run,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if message_template is not UNSET:
            field_dict["message_template"] = message_template

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_cron_trigger_target import AgentCronTriggerTarget
        from ..models.agent_profile_cron_trigger_target import (
            AgentProfileCronTriggerTarget,
        )
        from ..models.cron_trigger_failure_report import CronTriggerFailureReport
        from ..models.cron_trigger_last_run import CronTriggerLastRun
        from ..models.integration_cron_trigger_target import (
            IntegrationCronTriggerTarget,
        )

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        name = d.pop("name")

        def _parse_target(
            data: object,
        ) -> Union[
            "AgentCronTriggerTarget",
            "AgentProfileCronTriggerTarget",
            "IntegrationCronTriggerTarget",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_cron_trigger_target_type_0 = (
                    AgentCronTriggerTarget.from_dict(data)
                )

                return componentsschemas_cron_trigger_target_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_cron_trigger_target_type_1 = (
                    AgentProfileCronTriggerTarget.from_dict(data)
                )

                return componentsschemas_cron_trigger_target_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_cron_trigger_target_type_2 = (
                IntegrationCronTriggerTarget.from_dict(data)
            )

            return componentsschemas_cron_trigger_target_type_2

        target = _parse_target(d.pop("target"))

        cron = d.pop("cron")

        timezone = d.pop("timezone")

        enabled = d.pop("enabled")

        def _parse_last_fired_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_fired_at_type_0 = isoparse(data)

                return last_fired_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_fired_at = _parse_last_fired_at(d.pop("last_fired_at"))

        def _parse_next_fire_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_fire_at_type_0 = isoparse(data)

                return next_fire_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        next_fire_at = _parse_next_fire_at(d.pop("next_fire_at"))

        def _parse_failure_report(
            data: object,
        ) -> Union["CronTriggerFailureReport", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                failure_report_type_0 = CronTriggerFailureReport.from_dict(data)

                return failure_report_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CronTriggerFailureReport", None], data)

        failure_report = _parse_failure_report(d.pop("failure_report"))

        def _parse_last_run(data: object) -> Union["CronTriggerLastRun", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_run_type_0 = CronTriggerLastRun.from_dict(data)

                return last_run_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CronTriggerLastRun", None], data)

        last_run = _parse_last_run(d.pop("last_run"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        message_template = d.pop("message_template", UNSET)

        cron_trigger = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            name=name,
            target=target,
            cron=cron,
            timezone=timezone,
            enabled=enabled,
            last_fired_at=last_fired_at,
            next_fire_at=next_fire_at,
            failure_report=failure_report,
            last_run=last_run,
            created_at=created_at,
            updated_at=updated_at,
            message_template=message_template,
        )

        return cron_trigger
