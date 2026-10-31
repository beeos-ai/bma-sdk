from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_cron_trigger_target import AgentCronTriggerTarget
    from ..models.agent_profile_cron_trigger_target import AgentProfileCronTriggerTarget
    from ..models.integration_cron_trigger_target import IntegrationCronTriggerTarget


T = TypeVar("T", bound="CreateCronTriggerRequest")


@_attrs_define
class CreateCronTriggerRequest:
    """
    Attributes:
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        target (Union['AgentCronTriggerTarget', 'AgentProfileCronTriggerTarget', 'IntegrationCronTriggerTarget']): What
            each firing does: type agent sends the message to an existing agent, type profile launches a new agent from a
            profile, and type integration hands the firing to an integration, such as a new Slack or Discord thread.
        cron (str): Standard five-field cron expression (minute, hour, day of month, month, day of week).
            `TZ=`/`CRON_TZ=` prefixes are rejected; set the `timezone` field instead.
        timezone (Union[Unset, str]): IANA time zone the schedule is evaluated in.
        message_template (Union[Unset, str]): Go text/template rendered on each firing to produce the message sent to
            the target. The template receives a `trigger` value with `name`, `fired_at`, `last_fired_at`, and `local_date`
            fields. Timestamps remain UTC; local_date is the scheduled occurrence's ISO date in the schedule timezone.
            Required for agent and profile targets; omitted for integration targets, which use their own settings. Rendering
            is capped at 64 KiB of output and one second of wall-clock time, and `printf` width and precision specifiers are
            capped at 1024; a firing whose template fails to render is recorded in `failure_report` without sending a
            message.
        enabled (Union[Unset, bool]): Whether the trigger fires on schedule; false pauses it. Default: True.
    """

    name: str
    target: Union[
        "AgentCronTriggerTarget",
        "AgentProfileCronTriggerTarget",
        "IntegrationCronTriggerTarget",
    ]
    cron: str
    timezone: Union[Unset, str] = UNSET
    message_template: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = True

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_cron_trigger_target import AgentCronTriggerTarget
        from ..models.agent_profile_cron_trigger_target import (
            AgentProfileCronTriggerTarget,
        )

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

        message_template = self.message_template

        enabled = self.enabled

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "target": target,
                "cron": cron,
            }
        )
        if timezone is not UNSET:
            field_dict["timezone"] = timezone
        if message_template is not UNSET:
            field_dict["message_template"] = message_template
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_cron_trigger_target import AgentCronTriggerTarget
        from ..models.agent_profile_cron_trigger_target import (
            AgentProfileCronTriggerTarget,
        )
        from ..models.integration_cron_trigger_target import (
            IntegrationCronTriggerTarget,
        )

        d = dict(src_dict)
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

        timezone = d.pop("timezone", UNSET)

        message_template = d.pop("message_template", UNSET)

        enabled = d.pop("enabled", UNSET)

        create_cron_trigger_request = cls(
            name=name,
            target=target,
            cron=cron,
            timezone=timezone,
            message_template=message_template,
            enabled=enabled,
        )

        return create_cron_trigger_request
