from typing import Literal, cast

AgentProfileCronTriggerTargetType = Literal["profile"]

AGENT_PROFILE_CRON_TRIGGER_TARGET_TYPE_VALUES: set[
    AgentProfileCronTriggerTargetType
] = {
    "profile",
}


def check_agent_profile_cron_trigger_target_type(
    value: str,
) -> AgentProfileCronTriggerTargetType:
    if value in AGENT_PROFILE_CRON_TRIGGER_TARGET_TYPE_VALUES:
        return cast(AgentProfileCronTriggerTargetType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_PROFILE_CRON_TRIGGER_TARGET_TYPE_VALUES!r}"
    )
