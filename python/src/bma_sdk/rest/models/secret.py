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

from ..models.management_kind import ManagementKind, check_management_kind
from ..models.secret_kind import SecretKind, check_secret_kind

if TYPE_CHECKING:
    from ..models.metadata import Metadata
    from ..models.org_secret_owner import OrgSecretOwner
    from ..models.project_secret_owner import ProjectSecretOwner
    from ..models.user_secret_owner import UserSecretOwner


T = TypeVar("T", bound="Secret")


@_attrs_define
class Secret:
    """
    Attributes:
        id (str): Secret ID (sec_...).
        org_id (str):
        management_kind (ManagementKind): Lifecycle owner. Tenant-managed resources can be changed through tenant APIs.
            Cluster-managed resources are installed and lifecycle-managed by the control plane; individual APIs may
            explicitly expose tenant-editable settings.
        owner (Union['OrgSecretOwner', 'ProjectSecretOwner', 'UserSecretOwner']):
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        kind (SecretKind):
        metadata (Metadata): Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64 characters, values must be
            strings of up to 512 characters.
        current_version_number (int):
        payload_keys (list[str]):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: str
    org_id: str
    management_kind: ManagementKind
    owner: Union["OrgSecretOwner", "ProjectSecretOwner", "UserSecretOwner"]
    name: str
    kind: SecretKind
    metadata: "Metadata"
    current_version_number: int
    payload_keys: list[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        from ..models.org_secret_owner import OrgSecretOwner
        from ..models.project_secret_owner import ProjectSecretOwner

        id = self.id

        org_id = self.org_id

        management_kind: str = self.management_kind

        owner: dict[str, Any]
        if isinstance(self.owner, OrgSecretOwner):
            owner = self.owner.to_dict()
        elif isinstance(self.owner, ProjectSecretOwner):
            owner = self.owner.to_dict()
        else:
            owner = self.owner.to_dict()

        name = self.name

        kind: str = self.kind

        metadata = self.metadata.to_dict()

        current_version_number = self.current_version_number

        payload_keys = self.payload_keys

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "management_kind": management_kind,
                "owner": owner,
                "name": name,
                "kind": kind,
                "metadata": metadata,
                "current_version_number": current_version_number,
                "payload_keys": payload_keys,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata import Metadata
        from ..models.org_secret_owner import OrgSecretOwner
        from ..models.project_secret_owner import ProjectSecretOwner
        from ..models.user_secret_owner import UserSecretOwner

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        management_kind = check_management_kind(d.pop("management_kind"))

        def _parse_owner(
            data: object,
        ) -> Union["OrgSecretOwner", "ProjectSecretOwner", "UserSecretOwner"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_secret_owner_type_0 = OrgSecretOwner.from_dict(data)

                return componentsschemas_secret_owner_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_secret_owner_type_1 = ProjectSecretOwner.from_dict(
                    data
                )

                return componentsschemas_secret_owner_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_secret_owner_type_2 = UserSecretOwner.from_dict(data)

            return componentsschemas_secret_owner_type_2

        owner = _parse_owner(d.pop("owner"))

        name = d.pop("name")

        kind = check_secret_kind(d.pop("kind"))

        metadata = Metadata.from_dict(d.pop("metadata"))

        current_version_number = d.pop("current_version_number")

        payload_keys = cast(list[str], d.pop("payload_keys"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        secret = cls(
            id=id,
            org_id=org_id,
            management_kind=management_kind,
            owner=owner,
            name=name,
            kind=kind,
            metadata=metadata,
            current_version_number=current_version_number,
            payload_keys=payload_keys,
            created_at=created_at,
            updated_at=updated_at,
        )

        return secret
