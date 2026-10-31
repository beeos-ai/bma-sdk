from typing import Literal, cast

DirectSecretAvailabilitySource = Literal["direct"]

DIRECT_SECRET_AVAILABILITY_SOURCE_VALUES: set[DirectSecretAvailabilitySource] = {
    "direct",
}


def check_direct_secret_availability_source(
    value: str,
) -> DirectSecretAvailabilitySource:
    if value in DIRECT_SECRET_AVAILABILITY_SOURCE_VALUES:
        return cast(DirectSecretAvailabilitySource, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {DIRECT_SECRET_AVAILABILITY_SOURCE_VALUES!r}"
    )
