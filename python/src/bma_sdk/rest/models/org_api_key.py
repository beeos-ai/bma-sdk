import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="OrgAPIKey")


@_attrs_define
class OrgAPIKey:
    """
    Attributes:
        id (str):
        org_id (str):
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        token_id (str): Stable non-secret display identifier. It is not embedded in the bearer token.
        org_role (str): The key's org role (admin or member). Empty for revoked keys.
        created_by_user_id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        last_used_at (Union[None, datetime.datetime]):
        revoked_at (Union[None, datetime.datetime]):
    """

    id: str
    org_id: str
    name: str
    token_id: str
    org_role: str
    created_by_user_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    last_used_at: Union[None, datetime.datetime]
    revoked_at: Union[None, datetime.datetime]

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        name = self.name

        token_id = self.token_id

        org_role = self.org_role

        created_by_user_id = self.created_by_user_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        last_used_at: Union[None, str]
        if isinstance(self.last_used_at, datetime.datetime):
            last_used_at = self.last_used_at.isoformat()
        else:
            last_used_at = self.last_used_at

        revoked_at: Union[None, str]
        if isinstance(self.revoked_at, datetime.datetime):
            revoked_at = self.revoked_at.isoformat()
        else:
            revoked_at = self.revoked_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "name": name,
                "token_id": token_id,
                "org_role": org_role,
                "created_by_user_id": created_by_user_id,
                "created_at": created_at,
                "updated_at": updated_at,
                "last_used_at": last_used_at,
                "revoked_at": revoked_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        name = d.pop("name")

        token_id = d.pop("token_id")

        org_role = d.pop("org_role")

        created_by_user_id = d.pop("created_by_user_id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_last_used_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_used_at_type_0 = isoparse(data)

                return last_used_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_used_at = _parse_last_used_at(d.pop("last_used_at"))

        def _parse_revoked_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                revoked_at_type_0 = isoparse(data)

                return revoked_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        revoked_at = _parse_revoked_at(d.pop("revoked_at"))

        org_api_key = cls(
            id=id,
            org_id=org_id,
            name=name,
            token_id=token_id,
            org_role=org_role,
            created_by_user_id=created_by_user_id,
            created_at=created_at,
            updated_at=updated_at,
            last_used_at=last_used_at,
            revoked_at=revoked_at,
        )

        return org_api_key
