from typing import Literal, cast

GrantedSecretAvailabilitySource = Literal["grant"]

GRANTED_SECRET_AVAILABILITY_SOURCE_VALUES: set[GrantedSecretAvailabilitySource] = {
    "grant",
}


def check_granted_secret_availability_source(
    value: str,
) -> GrantedSecretAvailabilitySource:
    if value in GRANTED_SECRET_AVAILABILITY_SOURCE_VALUES:
        return cast(GrantedSecretAvailabilitySource, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GRANTED_SECRET_AVAILABILITY_SOURCE_VALUES!r}"
    )
