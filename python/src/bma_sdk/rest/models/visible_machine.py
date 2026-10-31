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
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.machine_connection_state import (
    MachineConnectionState,
    check_machine_connection_state,
)
from ..models.machine_lifecycle_state import (
    MachineLifecycleState,
    check_machine_lifecycle_state,
)
from ..models.machine_source_kind import MachineSourceKind, check_machine_source_kind

if TYPE_CHECKING:
    from ..models.machine_access import MachineAccess


T = TypeVar("T", bound="VisibleMachine")


@_attrs_define
class VisibleMachine:
    """
    Attributes:
        id (str): Machine ID (mch_...).
        org_id (str):
        source_kind (MachineSourceKind):
        display_name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        description (str):
        provider (str):
        lifecycle_state (MachineLifecycleState):
        connection_state (MachineConnectionState):
        last_observed_at (Union[None, datetime.datetime]):
        deleted_at (Union[None, datetime.datetime]):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        access (MachineAccess):
    """

    id: str
    org_id: str
    source_kind: MachineSourceKind
    display_name: str
    description: str
    provider: str
    lifecycle_state: MachineLifecycleState
    connection_state: MachineConnectionState
    last_observed_at: Union[None, datetime.datetime]
    deleted_at: Union[None, datetime.datetime]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    access: "MachineAccess"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        source_kind: str = self.source_kind

        display_name = self.display_name

        description = self.description

        provider = self.provider

        lifecycle_state: str = self.lifecycle_state

        connection_state: str = self.connection_state

        last_observed_at: Union[None, str]
        if isinstance(self.last_observed_at, datetime.datetime):
            last_observed_at = self.last_observed_at.isoformat()
        else:
            last_observed_at = self.last_observed_at

        deleted_at: Union[None, str]
        if isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        access = self.access.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "source_kind": source_kind,
                "display_name": display_name,
                "description": description,
                "provider": provider,
                "lifecycle_state": lifecycle_state,
                "connection_state": connection_state,
                "last_observed_at": last_observed_at,
                "deleted_at": deleted_at,
                "created_at": created_at,
                "updated_at": updated_at,
                "access": access,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.machine_access import MachineAccess

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        source_kind = check_machine_source_kind(d.pop("source_kind"))

        display_name = d.pop("display_name")

        description = d.pop("description")

        provider = d.pop("provider")

        lifecycle_state = check_machine_lifecycle_state(d.pop("lifecycle_state"))

        connection_state = check_machine_connection_state(d.pop("connection_state"))

        def _parse_last_observed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_observed_at_type_0 = isoparse(data)

                return last_observed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_observed_at = _parse_last_observed_at(d.pop("last_observed_at"))

        def _parse_deleted_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_at_type_0 = isoparse(data)

                return deleted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        access = MachineAccess.from_dict(d.pop("access"))

        visible_machine = cls(
            id=id,
            org_id=org_id,
            source_kind=source_kind,
            display_name=display_name,
            description=description,
            provider=provider,
            lifecycle_state=lifecycle_state,
            connection_state=connection_state,
            last_observed_at=last_observed_at,
            deleted_at=deleted_at,
            created_at=created_at,
            updated_at=updated_at,
            access=access,
        )

        visible_machine.additional_properties = d
        return visible_machine

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
