from typing import Literal, cast

OrgAPIKeyRole = Literal["admin", "member"]

ORG_API_KEY_ROLE_VALUES: set[OrgAPIKeyRole] = {
    "admin",
    "member",
}


def check_org_api_key_role(value: str) -> OrgAPIKeyRole:
    if value in ORG_API_KEY_ROLE_VALUES:
        return cast(OrgAPIKeyRole, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ORG_API_KEY_ROLE_VALUES!r}"
    )
