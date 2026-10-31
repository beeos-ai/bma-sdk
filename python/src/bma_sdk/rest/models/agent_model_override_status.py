from typing import Literal, cast

AgentModelOverrideStatus = Literal["active", "expired", "revoked"]

AGENT_MODEL_OVERRIDE_STATUS_VALUES: set[AgentModelOverrideStatus] = {
    "active",
    "expired",
    "revoked",
}


def check_agent_model_override_status(value: str) -> AgentModelOverrideStatus:
    if value in AGENT_MODEL_OVERRIDE_STATUS_VALUES:
        return cast(AgentModelOverrideStatus, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {AGENT_MODEL_OVERRIDE_STATUS_VALUES!r}"
    )
