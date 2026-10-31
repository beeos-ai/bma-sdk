from typing import Literal, cast

ActorProvider = Literal["bma", "external", "integration"]

ACTOR_PROVIDER_VALUES: set[ActorProvider] = {
    "bma",
    "external",
    "integration",
}


def check_actor_provider(value: str) -> ActorProvider:
    if value in ACTOR_PROVIDER_VALUES:
        return cast(ActorProvider, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ACTOR_PROVIDER_VALUES!r}"
    )
