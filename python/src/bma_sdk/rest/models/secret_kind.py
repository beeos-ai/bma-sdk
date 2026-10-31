from typing import Literal, cast

SecretKind = Literal[
    "aws_credentials",
    "generic",
    "github_app_credentials",
    "oauth_token_set",
    "slack_app_credentials",
]

SECRET_KIND_VALUES: set[SecretKind] = {
    "aws_credentials",
    "generic",
    "github_app_credentials",
    "oauth_token_set",
    "slack_app_credentials",
}


def check_secret_kind(value: str) -> SecretKind:
    if value in SECRET_KIND_VALUES:
        return cast(SecretKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {SECRET_KIND_VALUES!r}"
    )
