from typing import Literal, cast

AgentCronTriggerTargetType = Literal["agent"]

AGENT_CRON_TRIGGER_TARGET_TYPE_VALUES: set[AgentCronTriggerTargetType] = {
    "agent",
}


def check_agent_cron_trigger_target_type(value: str) -> AgentCronTriggerTargetType:
    if value in AGENT_CRON_TRIGGER_TARGET_TYPE_VALUES:
        return cast(AgentCronTriggerTargetType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_CRON_TRIGGER_TARGET_TYPE_VALUES!r}"
    )
