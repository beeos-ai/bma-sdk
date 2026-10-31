from typing import Literal, cast

GitHubAppCredentialsSecretMaterialKind = Literal["github_app_credentials"]

GIT_HUB_APP_CREDENTIALS_SECRET_MATERIAL_KIND_VALUES: set[
    GitHubAppCredentialsSecretMaterialKind
] = {
    "github_app_credentials",
}


def check_git_hub_app_credentials_secret_material_kind(
    value: str,
) -> GitHubAppCredentialsSecretMaterialKind:
    if value in GIT_HUB_APP_CREDENTIALS_SECRET_MATERIAL_KIND_VALUES:
        return cast(GitHubAppCredentialsSecretMaterialKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {GIT_HUB_APP_CREDENTIALS_SECRET_MATERIAL_KIND_VALUES!r}"
    )
