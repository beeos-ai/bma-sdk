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

from ..models.machine_connection_state import (
    MachineConnectionState,
    check_machine_connection_state,
)
from ..models.machine_lifecycle_state import (
    MachineLifecycleState,
    check_machine_lifecycle_state,
)
from ..models.machine_source_kind import MachineSourceKind, check_machine_source_kind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.machine_env import MachineEnv
    from ..models.machine_failure_report import MachineFailureReport
    from ..models.machine_secret_env import MachineSecretEnv
    from ..models.metadata import Metadata


T = TypeVar("T", bound="Machine")


@_attrs_define
class Machine:
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
        cwd (str):
        env (MachineEnv):
        secret_env (MachineSecretEnv):
        lifecycle_reason_code (str):
        lifecycle_reason_message (str):
        next_reconcile_after (Union[None, datetime.datetime]):
        provision_attempts (int):
        delete_attempts (int):
        metadata (Metadata): Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64 characters, values must be
            strings of up to 512 characters.
        deleted_at (Union[None, datetime.datetime]):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        machine_pool_id (Union[None, Unset, str]):
        connection_state_reason (Union[Unset, str]):
        failure_report (Union[Unset, MachineFailureReport]): The machine's most recent daemon-reported failure. A single
            slot, overwritten by newer reports. Runtime crash reports remain as historical diagnostics; recovery may clear
            other failure stages.
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
    cwd: str
    env: "MachineEnv"
    secret_env: "MachineSecretEnv"
    lifecycle_reason_code: str
    lifecycle_reason_message: str
    next_reconcile_after: Union[None, datetime.datetime]
    provision_attempts: int
    delete_attempts: int
    metadata: "Metadata"
    deleted_at: Union[None, datetime.datetime]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    machine_pool_id: Union[None, Unset, str] = UNSET
    connection_state_reason: Union[Unset, str] = UNSET
    failure_report: Union[Unset, "MachineFailureReport"] = UNSET

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

        cwd = self.cwd

        env = self.env.to_dict()

        secret_env = self.secret_env.to_dict()

        lifecycle_reason_code = self.lifecycle_reason_code

        lifecycle_reason_message = self.lifecycle_reason_message

        next_reconcile_after: Union[None, str]
        if isinstance(self.next_reconcile_after, datetime.datetime):
            next_reconcile_after = self.next_reconcile_after.isoformat()
        else:
            next_reconcile_after = self.next_reconcile_after

        provision_attempts = self.provision_attempts

        delete_attempts = self.delete_attempts

        metadata = self.metadata.to_dict()

        deleted_at: Union[None, str]
        if isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        machine_pool_id: Union[None, Unset, str]
        if isinstance(self.machine_pool_id, Unset):
            machine_pool_id = UNSET
        else:
            machine_pool_id = self.machine_pool_id

        connection_state_reason = self.connection_state_reason

        failure_report: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.failure_report, Unset):
            failure_report = self.failure_report.to_dict()

        field_dict: dict[str, Any] = {}

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
                "cwd": cwd,
                "env": env,
                "secret_env": secret_env,
                "lifecycle_reason_code": lifecycle_reason_code,
                "lifecycle_reason_message": lifecycle_reason_message,
                "next_reconcile_after": next_reconcile_after,
                "provision_attempts": provision_attempts,
                "delete_attempts": delete_attempts,
                "metadata": metadata,
                "deleted_at": deleted_at,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if machine_pool_id is not UNSET:
            field_dict["machine_pool_id"] = machine_pool_id
        if connection_state_reason is not UNSET:
            field_dict["connection_state_reason"] = connection_state_reason
        if failure_report is not UNSET:
            field_dict["failure_report"] = failure_report

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.machine_env import MachineEnv
        from ..models.machine_failure_report import MachineFailureReport
        from ..models.machine_secret_env import MachineSecretEnv
        from ..models.metadata import Metadata

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

        cwd = d.pop("cwd")

        env = MachineEnv.from_dict(d.pop("env"))

        secret_env = MachineSecretEnv.from_dict(d.pop("secret_env"))

        lifecycle_reason_code = d.pop("lifecycle_reason_code")

        lifecycle_reason_message = d.pop("lifecycle_reason_message")

        def _parse_next_reconcile_after(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_reconcile_after_type_0 = isoparse(data)

                return next_reconcile_after_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        next_reconcile_after = _parse_next_reconcile_after(
            d.pop("next_reconcile_after")
        )

        provision_attempts = d.pop("provision_attempts")

        delete_attempts = d.pop("delete_attempts")

        metadata = Metadata.from_dict(d.pop("metadata"))

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

        def _parse_machine_pool_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        machine_pool_id = _parse_machine_pool_id(d.pop("machine_pool_id", UNSET))

        connection_state_reason = d.pop("connection_state_reason", UNSET)

        _failure_report = d.pop("failure_report", UNSET)
        failure_report: Union[Unset, MachineFailureReport]
        if isinstance(_failure_report, Unset):
            failure_report = UNSET
        else:
            failure_report = MachineFailureReport.from_dict(_failure_report)

        machine = cls(
            id=id,
            org_id=org_id,
            source_kind=source_kind,
            display_name=display_name,
            description=description,
            provider=provider,
            lifecycle_state=lifecycle_state,
            connection_state=connection_state,
            last_observed_at=last_observed_at,
            cwd=cwd,
            env=env,
            secret_env=secret_env,
            lifecycle_reason_code=lifecycle_reason_code,
            lifecycle_reason_message=lifecycle_reason_message,
            next_reconcile_after=next_reconcile_after,
            provision_attempts=provision_attempts,
            delete_attempts=delete_attempts,
            metadata=metadata,
            deleted_at=deleted_at,
            created_at=created_at,
            updated_at=updated_at,
            machine_pool_id=machine_pool_id,
            connection_state_reason=connection_state_reason,
            failure_report=failure_report,
        )

        return machine
