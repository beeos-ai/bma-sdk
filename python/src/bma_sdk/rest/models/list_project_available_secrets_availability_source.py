from typing import Literal, cast

ListProjectAvailableSecretsAvailabilitySource = Literal["direct", "grant"]

LIST_PROJECT_AVAILABLE_SECRETS_AVAILABILITY_SOURCE_VALUES: set[
    ListProjectAvailableSecretsAvailabilitySource
] = {
    "direct",
    "grant",
}


def check_list_project_available_secrets_availability_source(
    value: str,
) -> ListProjectAvailableSecretsAvailabilitySource:
    if value in LIST_PROJECT_AVAILABLE_SECRETS_AVAILABILITY_SOURCE_VALUES:
        return cast(ListProjectAvailableSecretsAvailabilitySource, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {LIST_PROJECT_AVAILABLE_SECRETS_AVAILABILITY_SOURCE_VALUES!r}"
    )
