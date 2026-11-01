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
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.machine_pool_default_machine_env import MachinePoolDefaultMachineEnv
    from ..models.machine_pool_default_machine_provider_options import (
        MachinePoolDefaultMachineProviderOptions,
    )
    from ..models.machine_pool_default_machine_secret_env import (
        MachinePoolDefaultMachineSecretEnv,
    )
    from ..models.machine_pool_provider_config import MachinePoolProviderConfig
    from ..models.machine_pool_usage import MachinePoolUsage
    from ..models.metadata import Metadata


T = TypeVar("T", bound="MachinePool")


@_attrs_define
class MachinePool:
    """
    Attributes:
        id (str): Machine pool ID (mpo_...).
        org_id (str):
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        management_kind (ManagementKind): Lifecycle owner. Tenant-managed resources can be changed through tenant APIs.
            Cluster-managed resources are installed and lifecycle-managed by the control plane; individual APIs may
            explicitly expose tenant-editable settings.
        description (str):
        provider (str):
        default_machine_cpu (Union[None, int]):
        default_machine_memory_mb (Union[None, int]):
        default_machine_env (MachinePoolDefaultMachineEnv): Default environment for pool machines. A machine's
            environment, including resolved secret_env values, is applied to the provider machine at provisioning, so the
            provider_options startup_script and the daemon run with it, and is resolved again for each process at launch.
        default_machine_secret_env (MachinePoolDefaultMachineSecretEnv): Default secret environment for pool machines,
            mapping env names to generic secret references. References are resolved to secret values wherever the machine
            environment is applied.
        default_machine_provider_options (MachinePoolDefaultMachineProviderOptions):
        default_cwd (str):
        provider_config (MachinePoolProviderConfig):
        runtime_protection_enabled (bool): Whether BMA deletes this pool's machines when the provider remains running
            after the daemon becomes inactive.
        max_total_machines (int): Deprecated, not enforced: how many machines a pool has no longer blocks new machines.
            Organization and project quotas over in-use machines (org resource limits max_in_use_pool_machines_per_project
            and max_in_use_pool_machines_per_org) govern capacity.
        max_total_cpu (Union[None, int]): Deprecated, not enforced: organization and project in-use machine CPU quotas
            govern capacity.
        max_total_memory_mb (Union[None, int]): Deprecated, not enforced: organization and project in-use machine memory
            quotas govern capacity.
        min_machine_cpu (Union[None, int]):
        min_machine_memory_mb (Union[None, int]):
        max_machine_cpu (Union[None, int]):
        max_machine_memory_mb (Union[None, int]):
        delete_after_idle_minutes (Union[None, int]): Idle minutes before deleting a machine from this pool, or null
            when the pool default is unset.
        pause_after_idle_minutes (Union[None, int]): Idle minutes before pausing a machine from this pool, or null when
            the pool does not pause idle machines.
        archive_after_paused_days (Union[None, int]): Days a machine stays paused before it is archived, or null when
            the pool does not archive.
        delete_after_paused_days (Union[None, int]): Age in days, counted from the machine's creation, after which a
            paused machine is deleted, or null when the pool keeps paused machines.
        metadata (Metadata): Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64 characters, values must be
            strings of up to 512 characters.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        provider_auth_secret_id (Union[Unset, str]): Secret ID (sec_...).
        usage (Union[Unset, MachinePoolUsage]):
    """

    id: str
    org_id: str
    name: str
    management_kind: ManagementKind
    description: str
    provider: str
    default_machine_cpu: Union[None, int]
    default_machine_memory_mb: Union[None, int]
    default_machine_env: "MachinePoolDefaultMachineEnv"
    default_machine_secret_env: "MachinePoolDefaultMachineSecretEnv"
    default_machine_provider_options: "MachinePoolDefaultMachineProviderOptions"
    default_cwd: str
    provider_config: "MachinePoolProviderConfig"
    runtime_protection_enabled: bool
    max_total_machines: int
    max_total_cpu: Union[None, int]
    max_total_memory_mb: Union[None, int]
    min_machine_cpu: Union[None, int]
    min_machine_memory_mb: Union[None, int]
    max_machine_cpu: Union[None, int]
    max_machine_memory_mb: Union[None, int]
    delete_after_idle_minutes: Union[None, int]
    pause_after_idle_minutes: Union[None, int]
    archive_after_paused_days: Union[None, int]
    delete_after_paused_days: Union[None, int]
    metadata: "Metadata"
    created_at: datetime.datetime
    updated_at: datetime.datetime
    provider_auth_secret_id: Union[Unset, str] = UNSET
    usage: Union[Unset, "MachinePoolUsage"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        name = self.name

        management_kind: str = self.management_kind

        description = self.description

        provider = self.provider

        default_machine_cpu: Union[None, int]
        default_machine_cpu = self.default_machine_cpu

        default_machine_memory_mb: Union[None, int]
        default_machine_memory_mb = self.default_machine_memory_mb

        default_machine_env = self.default_machine_env.to_dict()

        default_machine_secret_env = self.default_machine_secret_env.to_dict()

        default_machine_provider_options = (
            self.default_machine_provider_options.to_dict()
        )

        default_cwd = self.default_cwd

        provider_config = self.provider_config.to_dict()

        runtime_protection_enabled = self.runtime_protection_enabled

        max_total_machines = self.max_total_machines

        max_total_cpu: Union[None, int]
        max_total_cpu = self.max_total_cpu

        max_total_memory_mb: Union[None, int]
        max_total_memory_mb = self.max_total_memory_mb

        min_machine_cpu: Union[None, int]
        min_machine_cpu = self.min_machine_cpu

        min_machine_memory_mb: Union[None, int]
        min_machine_memory_mb = self.min_machine_memory_mb

        max_machine_cpu: Union[None, int]
        max_machine_cpu = self.max_machine_cpu

        max_machine_memory_mb: Union[None, int]
        max_machine_memory_mb = self.max_machine_memory_mb

        delete_after_idle_minutes: Union[None, int]
        delete_after_idle_minutes = self.delete_after_idle_minutes

        pause_after_idle_minutes: Union[None, int]
        pause_after_idle_minutes = self.pause_after_idle_minutes

        archive_after_paused_days: Union[None, int]
        archive_after_paused_days = self.archive_after_paused_days

        delete_after_paused_days: Union[None, int]
        delete_after_paused_days = self.delete_after_paused_days

        metadata = self.metadata.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        provider_auth_secret_id = self.provider_auth_secret_id

        usage: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "name": name,
                "management_kind": management_kind,
                "description": description,
                "provider": provider,
                "default_machine_cpu": default_machine_cpu,
                "default_machine_memory_mb": default_machine_memory_mb,
                "default_machine_env": default_machine_env,
                "default_machine_secret_env": default_machine_secret_env,
                "default_machine_provider_options": default_machine_provider_options,
                "default_cwd": default_cwd,
                "provider_config": provider_config,
                "runtime_protection_enabled": runtime_protection_enabled,
                "max_total_machines": max_total_machines,
                "max_total_cpu": max_total_cpu,
                "max_total_memory_mb": max_total_memory_mb,
                "min_machine_cpu": min_machine_cpu,
                "min_machine_memory_mb": min_machine_memory_mb,
                "max_machine_cpu": max_machine_cpu,
                "max_machine_memory_mb": max_machine_memory_mb,
                "delete_after_idle_minutes": delete_after_idle_minutes,
                "pause_after_idle_minutes": pause_after_idle_minutes,
                "archive_after_paused_days": archive_after_paused_days,
                "delete_after_paused_days": delete_after_paused_days,
                "metadata": metadata,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if provider_auth_secret_id is not UNSET:
            field_dict["provider_auth_secret_id"] = provider_auth_secret_id
        if usage is not UNSET:
            field_dict["usage"] = usage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.machine_pool_default_machine_env import (
            MachinePoolDefaultMachineEnv,
        )
        from ..models.machine_pool_default_machine_provider_options import (
            MachinePoolDefaultMachineProviderOptions,
        )
        from ..models.machine_pool_default_machine_secret_env import (
            MachinePoolDefaultMachineSecretEnv,
        )
        from ..models.machine_pool_provider_config import MachinePoolProviderConfig
        from ..models.machine_pool_usage import MachinePoolUsage
        from ..models.metadata import Metadata

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        name = d.pop("name")

        management_kind = check_management_kind(d.pop("management_kind"))

        description = d.pop("description")

        provider = d.pop("provider")

        def _parse_default_machine_cpu(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        default_machine_cpu = _parse_default_machine_cpu(d.pop("default_machine_cpu"))

        def _parse_default_machine_memory_mb(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        default_machine_memory_mb = _parse_default_machine_memory_mb(
            d.pop("default_machine_memory_mb")
        )

        default_machine_env = MachinePoolDefaultMachineEnv.from_dict(
            d.pop("default_machine_env")
        )

        default_machine_secret_env = MachinePoolDefaultMachineSecretEnv.from_dict(
            d.pop("default_machine_secret_env")
        )

        default_machine_provider_options = (
            MachinePoolDefaultMachineProviderOptions.from_dict(
                d.pop("default_machine_provider_options")
            )
        )

        default_cwd = d.pop("default_cwd")

        provider_config = MachinePoolProviderConfig.from_dict(d.pop("provider_config"))

        runtime_protection_enabled = d.pop("runtime_protection_enabled")

        max_total_machines = d.pop("max_total_machines")

        def _parse_max_total_cpu(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_total_cpu = _parse_max_total_cpu(d.pop("max_total_cpu"))

        def _parse_max_total_memory_mb(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_total_memory_mb = _parse_max_total_memory_mb(d.pop("max_total_memory_mb"))

        def _parse_min_machine_cpu(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        min_machine_cpu = _parse_min_machine_cpu(d.pop("min_machine_cpu"))

        def _parse_min_machine_memory_mb(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        min_machine_memory_mb = _parse_min_machine_memory_mb(
            d.pop("min_machine_memory_mb")
        )

        def _parse_max_machine_cpu(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_machine_cpu = _parse_max_machine_cpu(d.pop("max_machine_cpu"))

        def _parse_max_machine_memory_mb(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_machine_memory_mb = _parse_max_machine_memory_mb(
            d.pop("max_machine_memory_mb")
        )

        def _parse_delete_after_idle_minutes(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        delete_after_idle_minutes = _parse_delete_after_idle_minutes(
            d.pop("delete_after_idle_minutes")
        )

        def _parse_pause_after_idle_minutes(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        pause_after_idle_minutes = _parse_pause_after_idle_minutes(
            d.pop("pause_after_idle_minutes")
        )

        def _parse_archive_after_paused_days(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        archive_after_paused_days = _parse_archive_after_paused_days(
            d.pop("archive_after_paused_days")
        )

        def _parse_delete_after_paused_days(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        delete_after_paused_days = _parse_delete_after_paused_days(
            d.pop("delete_after_paused_days")
        )

        metadata = Metadata.from_dict(d.pop("metadata"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        provider_auth_secret_id = d.pop("provider_auth_secret_id", UNSET)

        _usage = d.pop("usage", UNSET)
        usage: Union[Unset, MachinePoolUsage]
        if isinstance(_usage, Unset):
            usage = UNSET
        else:
            usage = MachinePoolUsage.from_dict(_usage)

        machine_pool = cls(
            id=id,
            org_id=org_id,
            name=name,
            management_kind=management_kind,
            description=description,
            provider=provider,
            default_machine_cpu=default_machine_cpu,
            default_machine_memory_mb=default_machine_memory_mb,
            default_machine_env=default_machine_env,
            default_machine_secret_env=default_machine_secret_env,
            default_machine_provider_options=default_machine_provider_options,
            default_cwd=default_cwd,
            provider_config=provider_config,
            runtime_protection_enabled=runtime_protection_enabled,
            max_total_machines=max_total_machines,
            max_total_cpu=max_total_cpu,
            max_total_memory_mb=max_total_memory_mb,
            min_machine_cpu=min_machine_cpu,
            min_machine_memory_mb=min_machine_memory_mb,
            max_machine_cpu=max_machine_cpu,
            max_machine_memory_mb=max_machine_memory_mb,
            delete_after_idle_minutes=delete_after_idle_minutes,
            pause_after_idle_minutes=pause_after_idle_minutes,
            archive_after_paused_days=archive_after_paused_days,
            delete_after_paused_days=delete_after_paused_days,
            metadata=metadata,
            created_at=created_at,
            updated_at=updated_at,
            provider_auth_secret_id=provider_auth_secret_id,
            usage=usage,
        )

        return machine_pool
