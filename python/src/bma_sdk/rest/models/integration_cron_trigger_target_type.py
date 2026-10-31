from typing import Literal, cast

IntegrationCronTriggerTargetType = Literal["integration"]

INTEGRATION_CRON_TRIGGER_TARGET_TYPE_VALUES: set[IntegrationCronTriggerTargetType] = {
    "integration",
}


def check_integration_cron_trigger_target_type(
    value: str,
) -> IntegrationCronTriggerTargetType:
    if value in INTEGRATION_CRON_TRIGGER_TARGET_TYPE_VALUES:
        return cast(IntegrationCronTriggerTargetType, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {INTEGRATION_CRON_TRIGGER_TARGET_TYPE_VALUES!r}"
    )
