from typing import Literal, cast

OrgSkillOwnerKind = Literal["org"]

ORG_SKILL_OWNER_KIND_VALUES: set[OrgSkillOwnerKind] = {
    "org",
}


def check_org_skill_owner_kind(value: str) -> OrgSkillOwnerKind:
    if value in ORG_SKILL_OWNER_KIND_VALUES:
        return cast(OrgSkillOwnerKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ORG_SKILL_OWNER_KIND_VALUES!r}"
    )
