from typing import Literal, cast

OrgSkillOwnerInputKind = Literal["org"]

ORG_SKILL_OWNER_INPUT_KIND_VALUES: set[OrgSkillOwnerInputKind] = {
    "org",
}


def check_org_skill_owner_input_kind(value: str) -> OrgSkillOwnerInputKind:
    if value in ORG_SKILL_OWNER_INPUT_KIND_VALUES:
        return cast(OrgSkillOwnerInputKind, value)
    raise TypeError(
        f"Unexpected value {value!r}. Expected one of {ORG_SKILL_OWNER_INPUT_KIND_VALUES!r}"
    )
