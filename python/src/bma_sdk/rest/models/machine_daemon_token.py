import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.metadata import Metadata


T = TypeVar("T", bound="MachineDaemonToken")


@_attrs_define
class MachineDaemonToken:
    """
    Attributes:
        id (str):
        org_id (str):
        machine_id (str): Machine ID (mch_...).
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        metadata (Metadata): Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64 characters, values must be
            strings of up to 512 characters.
        created_at (datetime.datetime):
        last_used_at (Union[None, datetime.datetime]):
        revoked_at (Union[None, datetime.datetime]):
        revoke_reason (str):
    """

    id: str
    org_id: str
    machine_id: str
    name: str
    metadata: "Metadata"
    created_at: datetime.datetime
    last_used_at: Union[None, datetime.datetime]
    revoked_at: Union[None, datetime.datetime]
    revoke_reason: str

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        machine_id = self.machine_id

        name = self.name

        metadata = self.metadata.to_dict()

        created_at = self.created_at.isoformat()

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

        revoke_reason = self.revoke_reason

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "machine_id": machine_id,
                "name": name,
                "metadata": metadata,
                "created_at": created_at,
                "last_used_at": last_used_at,
                "revoked_at": revoked_at,
                "revoke_reason": revoke_reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata import Metadata

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        machine_id = d.pop("machine_id")

        name = d.pop("name")

        metadata = Metadata.from_dict(d.pop("metadata"))

        created_at = isoparse(d.pop("created_at"))

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

        revoke_reason = d.pop("revoke_reason")

        machine_daemon_token = cls(
            id=id,
            org_id=org_id,
            machine_id=machine_id,
            name=name,
            metadata=metadata,
            created_at=created_at,
            last_used_at=last_used_at,
            revoked_at=revoked_at,
            revoke_reason=revoke_reason,
        )

        return machine_daemon_token
