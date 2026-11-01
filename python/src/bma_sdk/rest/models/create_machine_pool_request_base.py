from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_machine_pool_request_base_default_machine_env import (
        CreateMachinePoolRequestBaseDefaultMachineEnv,
    )
    from ..models.create_machine_pool_request_base_default_machine_provider_options import (
        CreateMachinePoolRequestBaseDefaultMachineProviderOptions,
    )
    from ..models.create_machine_pool_request_base_default_machine_secret_env import (
        CreateMachinePoolRequestBaseDefaultMachineSecretEnv,
    )
    from ..models.create_machine_pool_request_base_provider_config import (
        CreateMachinePoolRequestBaseProviderConfig,
    )
    from ..models.machine_metadata import MachineMetadata


T = TypeVar("T", bound="CreateMachinePoolRequestBase")


@_attrs_define
class CreateMachinePoolRequestBase:
    """
    Attributes:
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        provider (str):
        default_machine_provider_options (CreateMachinePoolRequestBaseDefaultMachineProviderOptions):
        provider_auth_secret_id (str): Secret ID (sec_...).
        max_total_machines (int): Deprecated, not enforced: how many machines a pool has no longer blocks new machines.
            Organization and project quotas over in-use machines (org resource limits max_in_use_pool_machines_per_project
            and max_in_use_pool_machines_per_org) govern capacity.
        description (Union[Unset, str]):
        default_machine_cpu (Union[Unset, int]):
        default_machine_memory_mb (Union[Unset, int]):
        default_machine_env (Union[Unset, CreateMachinePoolRequestBaseDefaultMachineEnv]): Default environment for pool
            machines. A machine's environment, including resolved secret_env values, is applied to the provider machine at
            provisioning, so the provider_options startup_script and the daemon run with it, and is resolved again for each
            process at launch.
        default_machine_secret_env (Union[Unset, CreateMachinePoolRequestBaseDefaultMachineSecretEnv]): Default secret
            environment for pool machines, mapping env names to generic secret references. References are resolved to secret
            values wherever the machine environment is applied.
        default_cwd (Union[Unset, str]):
        provider_config (Union[Unset, CreateMachinePoolRequestBaseProviderConfig]):
        runtime_protection_enabled (Union[Unset, bool]): Whether BMA should delete a pool machine when its provider
            remains running after its daemon becomes inactive. Defaults to false when omitted. Default: False.
        max_total_cpu (Union[Unset, int]): Deprecated, not enforced: organization and project in-use machine CPU quotas
            govern capacity.
        max_total_memory_mb (Union[Unset, int]): Deprecated, not enforced: organization and project in-use machine
            memory quotas govern capacity.
        min_machine_cpu (Union[Unset, int]):
        min_machine_memory_mb (Union[Unset, int]):
        max_machine_cpu (Union[Unset, int]):
        max_machine_memory_mb (Union[Unset, int]):
        delete_after_idle_minutes (Union[Unset, int]): Idle minutes before deleting a machine from this pool. Omit to
            leave the pool default unset; a grant or agent source may still override it.
        pause_after_idle_minutes (Union[Unset, int]): Idle minutes before pausing a machine from this pool. A paused
            machine keeps its disk and resumes on the next command, terminal, desktop, or explicit resume. Exclusive with
            delete_after_idle_minutes; a grant or agent source delete policy still wins.
        archive_after_paused_days (Union[Unset, int]): Days a machine stays paused before it is archived. An archived
            machine is restored on the next access. Requires pause_after_idle_minutes.
        delete_after_paused_days (Union[Unset, int]): Delete a paused machine once it is this many days old, counted
            from the machine's creation (for a session machine, the session's start); activity does not extend it. A session
            that receives input after its machine was deleted gets a fresh machine. Requires pause_after_idle_minutes;
            cannot be combined with archive_after_paused_days.
        metadata (Union[Unset, MachineMetadata]): User-supplied metadata stored on a machine, provided directly or
            copied from the machine pool that provisions it. A restriction of Metadata that leaves room for one reserved
            pair - BMA sets observed_platform on the machine to the platform reported by its daemon, so the key is reserved
            and at most 15 user pairs are accepted.
    """

    name: str
    provider: str
    default_machine_provider_options: (
        "CreateMachinePoolRequestBaseDefaultMachineProviderOptions"
    )
    provider_auth_secret_id: str
    max_total_machines: int
    description: Union[Unset, str] = UNSET
    default_machine_cpu: Union[Unset, int] = UNSET
    default_machine_memory_mb: Union[Unset, int] = UNSET
    default_machine_env: Union[
        Unset, "CreateMachinePoolRequestBaseDefaultMachineEnv"
    ] = UNSET
    default_machine_secret_env: Union[
        Unset, "CreateMachinePoolRequestBaseDefaultMachineSecretEnv"
    ] = UNSET
    default_cwd: Union[Unset, str] = UNSET
    provider_config: Union[Unset, "CreateMachinePoolRequestBaseProviderConfig"] = UNSET
    runtime_protection_enabled: Union[Unset, bool] = False
    max_total_cpu: Union[Unset, int] = UNSET
    max_total_memory_mb: Union[Unset, int] = UNSET
    min_machine_cpu: Union[Unset, int] = UNSET
    min_machine_memory_mb: Union[Unset, int] = UNSET
    max_machine_cpu: Union[Unset, int] = UNSET
    max_machine_memory_mb: Union[Unset, int] = UNSET
    delete_after_idle_minutes: Union[Unset, int] = UNSET
    pause_after_idle_minutes: Union[Unset, int] = UNSET
    archive_after_paused_days: Union[Unset, int] = UNSET
    delete_after_paused_days: Union[Unset, int] = UNSET
    metadata: Union[Unset, "MachineMetadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        provider = self.provider

        default_machine_provider_options = (
            self.default_machine_provider_options.to_dict()
        )

        provider_auth_secret_id = self.provider_auth_secret_id

        max_total_machines = self.max_total_machines

        description = self.description

        default_machine_cpu = self.default_machine_cpu

        default_machine_memory_mb = self.default_machine_memory_mb

        default_machine_env: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.default_machine_env, Unset):
            default_machine_env = self.default_machine_env.to_dict()

        default_machine_secret_env: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.default_machine_secret_env, Unset):
            default_machine_secret_env = self.default_machine_secret_env.to_dict()

        default_cwd = self.default_cwd

        provider_config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.provider_config, Unset):
            provider_config = self.provider_config.to_dict()

        runtime_protection_enabled = self.runtime_protection_enabled

        max_total_cpu = self.max_total_cpu

        max_total_memory_mb = self.max_total_memory_mb

        min_machine_cpu = self.min_machine_cpu

        min_machine_memory_mb = self.min_machine_memory_mb

        max_machine_cpu = self.max_machine_cpu

        max_machine_memory_mb = self.max_machine_memory_mb

        delete_after_idle_minutes = self.delete_after_idle_minutes

        pause_after_idle_minutes = self.pause_after_idle_minutes

        archive_after_paused_days = self.archive_after_paused_days

        delete_after_paused_days = self.delete_after_paused_days

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "provider": provider,
                "default_machine_provider_options": default_machine_provider_options,
                "provider_auth_secret_id": provider_auth_secret_id,
                "max_total_machines": max_total_machines,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if default_machine_cpu is not UNSET:
            field_dict["default_machine_cpu"] = default_machine_cpu
        if default_machine_memory_mb is not UNSET:
            field_dict["default_machine_memory_mb"] = default_machine_memory_mb
        if default_machine_env is not UNSET:
            field_dict["default_machine_env"] = default_machine_env
        if default_machine_secret_env is not UNSET:
            field_dict["default_machine_secret_env"] = default_machine_secret_env
        if default_cwd is not UNSET:
            field_dict["default_cwd"] = default_cwd
        if provider_config is not UNSET:
            field_dict["provider_config"] = provider_config
        if runtime_protection_enabled is not UNSET:
            field_dict["runtime_protection_enabled"] = runtime_protection_enabled
        if max_total_cpu is not UNSET:
            field_dict["max_total_cpu"] = max_total_cpu
        if max_total_memory_mb is not UNSET:
            field_dict["max_total_memory_mb"] = max_total_memory_mb
        if min_machine_cpu is not UNSET:
            field_dict["min_machine_cpu"] = min_machine_cpu
        if min_machine_memory_mb is not UNSET:
            field_dict["min_machine_memory_mb"] = min_machine_memory_mb
        if max_machine_cpu is not UNSET:
            field_dict["max_machine_cpu"] = max_machine_cpu
        if max_machine_memory_mb is not UNSET:
            field_dict["max_machine_memory_mb"] = max_machine_memory_mb
        if delete_after_idle_minutes is not UNSET:
            field_dict["delete_after_idle_minutes"] = delete_after_idle_minutes
        if pause_after_idle_minutes is not UNSET:
            field_dict["pause_after_idle_minutes"] = pause_after_idle_minutes
        if archive_after_paused_days is not UNSET:
            field_dict["archive_after_paused_days"] = archive_after_paused_days
        if delete_after_paused_days is not UNSET:
            field_dict["delete_after_paused_days"] = delete_after_paused_days
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_machine_pool_request_base_default_machine_env import (
            CreateMachinePoolRequestBaseDefaultMachineEnv,
        )
        from ..models.create_machine_pool_request_base_default_machine_provider_options import (
            CreateMachinePoolRequestBaseDefaultMachineProviderOptions,
        )
        from ..models.create_machine_pool_request_base_default_machine_secret_env import (
            CreateMachinePoolRequestBaseDefaultMachineSecretEnv,
        )
        from ..models.create_machine_pool_request_base_provider_config import (
            CreateMachinePoolRequestBaseProviderConfig,
        )
        from ..models.machine_metadata import MachineMetadata

        d = dict(src_dict)
        name = d.pop("name")

        provider = d.pop("provider")

        default_machine_provider_options = (
            CreateMachinePoolRequestBaseDefaultMachineProviderOptions.from_dict(
                d.pop("default_machine_provider_options")
            )
        )

        provider_auth_secret_id = d.pop("provider_auth_secret_id")

        max_total_machines = d.pop("max_total_machines")

        description = d.pop("description", UNSET)

        default_machine_cpu = d.pop("default_machine_cpu", UNSET)

        default_machine_memory_mb = d.pop("default_machine_memory_mb", UNSET)

        _default_machine_env = d.pop("default_machine_env", UNSET)
        default_machine_env: Union[Unset, CreateMachinePoolRequestBaseDefaultMachineEnv]
        if isinstance(_default_machine_env, Unset):
            default_machine_env = UNSET
        else:
            default_machine_env = (
                CreateMachinePoolRequestBaseDefaultMachineEnv.from_dict(
                    _default_machine_env
                )
            )

        _default_machine_secret_env = d.pop("default_machine_secret_env", UNSET)
        default_machine_secret_env: Union[
            Unset, CreateMachinePoolRequestBaseDefaultMachineSecretEnv
        ]
        if isinstance(_default_machine_secret_env, Unset):
            default_machine_secret_env = UNSET
        else:
            default_machine_secret_env = (
                CreateMachinePoolRequestBaseDefaultMachineSecretEnv.from_dict(
                    _default_machine_secret_env
                )
            )

        default_cwd = d.pop("default_cwd", UNSET)

        _provider_config = d.pop("provider_config", UNSET)
        provider_config: Union[Unset, CreateMachinePoolRequestBaseProviderConfig]
        if isinstance(_provider_config, Unset):
            provider_config = UNSET
        else:
            provider_config = CreateMachinePoolRequestBaseProviderConfig.from_dict(
                _provider_config
            )

        runtime_protection_enabled = d.pop("runtime_protection_enabled", UNSET)

        max_total_cpu = d.pop("max_total_cpu", UNSET)

        max_total_memory_mb = d.pop("max_total_memory_mb", UNSET)

        min_machine_cpu = d.pop("min_machine_cpu", UNSET)

        min_machine_memory_mb = d.pop("min_machine_memory_mb", UNSET)

        max_machine_cpu = d.pop("max_machine_cpu", UNSET)

        max_machine_memory_mb = d.pop("max_machine_memory_mb", UNSET)

        delete_after_idle_minutes = d.pop("delete_after_idle_minutes", UNSET)

        pause_after_idle_minutes = d.pop("pause_after_idle_minutes", UNSET)

        archive_after_paused_days = d.pop("archive_after_paused_days", UNSET)

        delete_after_paused_days = d.pop("delete_after_paused_days", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, MachineMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = MachineMetadata.from_dict(_metadata)

        create_machine_pool_request_base = cls(
            name=name,
            provider=provider,
            default_machine_provider_options=default_machine_provider_options,
            provider_auth_secret_id=provider_auth_secret_id,
            max_total_machines=max_total_machines,
            description=description,
            default_machine_cpu=default_machine_cpu,
            default_machine_memory_mb=default_machine_memory_mb,
            default_machine_env=default_machine_env,
            default_machine_secret_env=default_machine_secret_env,
            default_cwd=default_cwd,
            provider_config=provider_config,
            runtime_protection_enabled=runtime_protection_enabled,
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
        )

        return create_machine_pool_request_base
