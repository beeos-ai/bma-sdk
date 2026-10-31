from typing import Literal, cast

OrgSecretOwnerKind = Literal["org"]

ORG_SECRET_OWNER_KIND_VALUES: set[OrgSecretOwnerKind] = {
    "org",
}


def check_org_secret_owner_kind(value: str) -> OrgSecretOwnerKind:
    if value in ORG_SECRET_OWNER_KIND_VALUES:
        return cast(OrgSecretOwnerKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ORG_SECRET_OWNER_KIND_VALUES!r}"
    )
