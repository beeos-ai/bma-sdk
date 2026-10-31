from typing import Literal, cast

OrgSecretOwnerInputKind = Literal["org"]

ORG_SECRET_OWNER_INPUT_KIND_VALUES: set[OrgSecretOwnerInputKind] = {
    "org",
}


def check_org_secret_owner_input_kind(value: str) -> OrgSecretOwnerInputKind:
    if value in ORG_SECRET_OWNER_INPUT_KIND_VALUES:
        return cast(OrgSecretOwnerInputKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ORG_SECRET_OWNER_INPUT_KIND_VALUES!r}"
    )
