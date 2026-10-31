from typing import Literal, cast

CronTriggerDeliveryMode = Literal["queued", "steering"]

CRON_TRIGGER_DELIVERY_MODE_VALUES: set[CronTriggerDeliveryMode] = {
    "queued",
    "steering",
}


def check_cron_trigger_delivery_mode(value: str) -> CronTriggerDeliveryMode:
    if value in CRON_TRIGGER_DELIVERY_MODE_VALUES:
        return cast(CronTriggerDeliveryMode, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {CRON_TRIGGER_DELIVERY_MODE_VALUES!r}"
    )
