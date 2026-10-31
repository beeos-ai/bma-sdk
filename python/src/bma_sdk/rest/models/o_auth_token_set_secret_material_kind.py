from typing import Literal, cast

OAuthTokenSetSecretMaterialKind = Literal["oauth_token_set"]

O_AUTH_TOKEN_SET_SECRET_MATERIAL_KIND_VALUES: set[OAuthTokenSetSecretMaterialKind] = {
    "oauth_token_set",
}


def check_o_auth_token_set_secret_material_kind(
    value: str,
) -> OAuthTokenSetSecretMaterialKind:
    if value in O_AUTH_TOKEN_SET_SECRET_MATERIAL_KIND_VALUES:
        return cast(OAuthTokenSetSecretMaterialKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {O_AUTH_TOKEN_SET_SECRET_MATERIAL_KIND_VALUES!r}"
    )
