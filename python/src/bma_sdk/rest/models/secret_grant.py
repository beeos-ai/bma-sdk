import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="SecretGrant")


@_attrs_define
class SecretGrant:
    """
    Attributes:
        id (str):
        org_id (str):
        secret_id (str): Secret ID (sec_...).
        target_project_id (str): Project ID (proj_...).
        created_at (datetime.datetime):
    """

    id: str
    org_id: str
    secret_id: str
    target_project_id: str
    created_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        secret_id = self.secret_id

        target_project_id = self.target_project_id

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "secret_id": secret_id,
                "target_project_id": target_project_id,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        secret_id = d.pop("secret_id")

        target_project_id = d.pop("target_project_id")

        created_at = isoparse(d.pop("created_at"))

        secret_grant = cls(
            id=id,
            org_id=org_id,
            secret_id=secret_id,
            target_project_id=target_project_id,
            created_at=created_at,
        )

        return secret_grant
