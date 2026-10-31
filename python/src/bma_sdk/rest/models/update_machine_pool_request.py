from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.machine_metadata import MachineMetadata
    from ..models.update_machine_pool_request_default_machine_env import (
        UpdateMachinePoolRequestDefaultMachineEnv,
    )
    from ..models.update_machine_pool_request_default_machine_provider_options import (
        UpdateMachinePoolRequestDefaultMachineProviderOptions,
    )
    from ..models.update_machine_pool_request_default_machine_secret_env import (
        UpdateMachinePoolRequestDefaultMachineSecretEnv,
    )
    from ..models.update_machine_pool_request_provider_config import (
        UpdateMachinePoolRequestProviderConfig,
    )


T = TypeVar("T", bound="UpdateMachinePoolRequest")


@_attrs_define
class UpdateMachinePoolRequest:
    """
    Attributes:
        name (Union[Unset, str]): Human-readable name. Spaces and punctuation are allowed; leading or trailing
            whitespace and invisible or control characters are not.
        description (Union[Unset, str]): Optional description of the pool.
        default_machine_cpu (Union[None, Unset, int]): Default CPU count for new machines in the pool.
        default_machine_memory_mb (Union[None, Unset, int]): Default memory in MB for new machines in the pool.
        default_machine_env (Union[Unset, UpdateMachinePoolRequestDefaultMachineEnv]): Default environment for pool
            machines. A machine's environment, including resolved secret_env values, is applied to the provider machine at
            provisioning, so the provider_options startup_script and the daemon run with it, and is resolved again for each
            process at launch.
        default_machine_secret_env (Union[Unset, UpdateMachinePoolRequestDefaultMachineSecretEnv]): Default secret
            environment for pool machines, mapping env names to generic secret references. References are resolved to secret
            values wherever the machine environment is applied.
        default_machine_provider_options (Union[Unset, UpdateMachinePoolRequestDefaultMachineProviderOptions]):
            Provider-specific options applied to new machines in the pool.
        default_cwd (Union[Unset, str]): Default working directory for processes on machines created from the pool after
            this change.
        provider_config (Union[Unset, UpdateMachinePoolRequestProviderConfig]): Provider-specific settings for the pool.
        provider_auth_secret_id (Union[Unset, str]): Secret ID (sec_...).
        runtime_protection_enabled (Union[Unset, bool]): Whether BMA should delete a pool machine when its provider
            remains running after its daemon becomes inactive.
        max_total_machines (Union[Unset, int]): Maximum number of live machines in the pool.
        max_total_cpu (Union[None, Unset, int]): Maximum total CPU across the pool's live machines.
        max_total_memory_mb (Union[None, Unset, int]): Maximum total memory in MB across the pool's live machines.
        min_machine_cpu (Union[None, Unset, int]): Smallest CPU count a single machine in the pool can use.
        min_machine_memory_mb (Union[None, Unset, int]): Smallest memory in MB a single machine in the pool can use.
        max_machine_cpu (Union[None, Unset, int]): Largest CPU count a single machine in the pool can use.
        max_machine_memory_mb (Union[None, Unset, int]): Largest memory in MB a single machine in the pool can use.
        delete_after_idle_minutes (Union[None, Unset, int]): Idle minutes before deleting a machine from this pool. Null
            clears the pool default; omitted leaves it unchanged.
        metadata (Union[Unset, MachineMetadata]): User-supplied metadata stored on a machine, provided directly or
            copied from the machine pool that provisions it. A restriction of Metadata that leaves room for one reserved
            pair - BMA sets observed_platform on the machine to the platform reported by its daemon, so the key is reserved
            and at most 15 user pairs are accepted.
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    default_machine_cpu: Union[None, Unset, int] = UNSET
    default_machine_memory_mb: Union[None, Unset, int] = UNSET
    default_machine_env: Union[Unset, "UpdateMachinePoolRequestDefaultMachineEnv"] = (
        UNSET
    )
    default_machine_secret_env: Union[
        Unset, "UpdateMachinePoolRequestDefaultMachineSecretEnv"
    ] = UNSET
    default_machine_provider_options: Union[
        Unset, "UpdateMachinePoolRequestDefaultMachineProviderOptions"
    ] = UNSET
    default_cwd: Union[Unset, str] = UNSET
    provider_config: Union[Unset, "UpdateMachinePoolRequestProviderConfig"] = UNSET
    provider_auth_secret_id: Union[Unset, str] = UNSET
    runtime_protection_enabled: Union[Unset, bool] = UNSET
    max_total_machines: Union[Unset, int] = UNSET
    max_total_cpu: Union[None, Unset, int] = UNSET
    max_total_memory_mb: Union[None, Unset, int] = UNSET
    min_machine_cpu: Union[None, Unset, int] = UNSET
    min_machine_memory_mb: Union[None, Unset, int] = UNSET
    max_machine_cpu: Union[None, Unset, int] = UNSET
    max_machine_memory_mb: Union[None, Unset, int] = UNSET
    delete_after_idle_minutes: Union[None, Unset, int] = UNSET
    metadata: Union[Unset, "MachineMetadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        default_machine_cpu: Union[None, Unset, int]
        if isinstance(self.default_machine_cpu, Unset):
            default_machine_cpu = UNSET
        else:
            default_machine_cpu = self.default_machine_cpu

        default_machine_memory_mb: Union[None, Unset, int]
        if isinstance(self.default_machine_memory_mb, Unset):
            default_machine_memory_mb = UNSET
        else:
            default_machine_memory_mb = self.default_machine_memory_mb

        default_machine_env: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.default_machine_env, Unset):
            default_machine_env = self.default_machine_env.to_dict()

        default_machine_secret_env: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.default_machine_secret_env, Unset):
            default_machine_secret_env = self.default_machine_secret_env.to_dict()

        default_machine_provider_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.default_machine_provider_options, Unset):
            default_machine_provider_options = (
                self.default_machine_provider_options.to_dict()
            )

        default_cwd = self.default_cwd

        provider_config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.provider_config, Unset):
            provider_config = self.provider_config.to_dict()

        provider_auth_secret_id = self.provider_auth_secret_id

        runtime_protection_enabled = self.runtime_protection_enabled

        max_total_machines = self.max_total_machines

        max_total_cpu: Union[None, Unset, int]
        if isinstance(self.max_total_cpu, Unset):
            max_total_cpu = UNSET
        else:
            max_total_cpu = self.max_total_cpu

        max_total_memory_mb: Union[None, Unset, int]
        if isinstance(self.max_total_memory_mb, Unset):
            max_total_memory_mb = UNSET
        else:
            max_total_memory_mb = self.max_total_memory_mb

        min_machine_cpu: Union[None, Unset, int]
        if isinstance(self.min_machine_cpu, Unset):
            min_machine_cpu = UNSET
        else:
            min_machine_cpu = self.min_machine_cpu

        min_machine_memory_mb: Union[None, Unset, int]
        if isinstance(self.min_machine_memory_mb, Unset):
            min_machine_memory_mb = UNSET
        else:
            min_machine_memory_mb = self.min_machine_memory_mb

        max_machine_cpu: Union[None, Unset, int]
        if isinstance(self.max_machine_cpu, Unset):
            max_machine_cpu = UNSET
        else:
            max_machine_cpu = self.max_machine_cpu

        max_machine_memory_mb: Union[None, Unset, int]
        if isinstance(self.max_machine_memory_mb, Unset):
            max_machine_memory_mb = UNSET
        else:
            max_machine_memory_mb = self.max_machine_memory_mb

        delete_after_idle_minutes: Union[None, Unset, int]
        if isinstance(self.delete_after_idle_minutes, Unset):
            delete_after_idle_minutes = UNSET
        else:
            delete_after_idle_minutes = self.delete_after_idle_minutes

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
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
        if default_machine_provider_options is not UNSET:
            field_dict["default_machine_provider_options"] = (
                default_machine_provider_options
            )
        if default_cwd is not UNSET:
            field_dict["default_cwd"] = default_cwd
        if provider_config is not UNSET:
            field_dict["provider_config"] = provider_config
        if provider_auth_secret_id is not UNSET:
            field_dict["provider_auth_secret_id"] = provider_auth_secret_id
        if runtime_protection_enabled is not UNSET:
            field_dict["runtime_protection_enabled"] = runtime_protection_enabled
        if max_total_machines is not UNSET:
            field_dict["max_total_machines"] = max_total_machines
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
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.machine_metadata import MachineMetadata
        from ..models.update_machine_pool_request_default_machine_env import (
            UpdateMachinePoolRequestDefaultMachineEnv,
        )
        from ..models.update_machine_pool_request_default_machine_provider_options import (
            UpdateMachinePoolRequestDefaultMachineProviderOptions,
        )
        from ..models.update_machine_pool_request_default_machine_secret_env import (
            UpdateMachinePoolRequestDefaultMachineSecretEnv,
        )
        from ..models.update_machine_pool_request_provider_config import (
            UpdateMachinePoolRequestProviderConfig,
        )

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        def _parse_default_machine_cpu(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        default_machine_cpu = _parse_default_machine_cpu(
            d.pop("default_machine_cpu", UNSET)
        )

        def _parse_default_machine_memory_mb(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        default_machine_memory_mb = _parse_default_machine_memory_mb(
            d.pop("default_machine_memory_mb", UNSET)
        )

        _default_machine_env = d.pop("default_machine_env", UNSET)
        default_machine_env: Union[Unset, UpdateMachinePoolRequestDefaultMachineEnv]
        if isinstance(_default_machine_env, Unset):
            default_machine_env = UNSET
        else:
            default_machine_env = UpdateMachinePoolRequestDefaultMachineEnv.from_dict(
                _default_machine_env
            )

        _default_machine_secret_env = d.pop("default_machine_secret_env", UNSET)
        default_machine_secret_env: Union[
            Unset, UpdateMachinePoolRequestDefaultMachineSecretEnv
        ]
        if isinstance(_default_machine_secret_env, Unset):
            default_machine_secret_env = UNSET
        else:
            default_machine_secret_env = (
                UpdateMachinePoolRequestDefaultMachineSecretEnv.from_dict(
                    _default_machine_secret_env
                )
            )

        _default_machine_provider_options = d.pop(
            "default_machine_provider_options", UNSET
        )
        default_machine_provider_options: Union[
            Unset, UpdateMachinePoolRequestDefaultMachineProviderOptions
        ]
        if isinstance(_default_machine_provider_options, Unset):
            default_machine_provider_options = UNSET
        else:
            default_machine_provider_options = (
                UpdateMachinePoolRequestDefaultMachineProviderOptions.from_dict(
                    _default_machine_provider_options
                )
            )

        default_cwd = d.pop("default_cwd", UNSET)

        _provider_config = d.pop("provider_config", UNSET)
        provider_config: Union[Unset, UpdateMachinePoolRequestProviderConfig]
        if isinstance(_provider_config, Unset):
            provider_config = UNSET
        else:
            provider_config = UpdateMachinePoolRequestProviderConfig.from_dict(
                _provider_config
            )

        provider_auth_secret_id = d.pop("provider_auth_secret_id", UNSET)

        runtime_protection_enabled = d.pop("runtime_protection_enabled", UNSET)

        max_total_machines = d.pop("max_total_machines", UNSET)

        def _parse_max_total_cpu(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_total_cpu = _parse_max_total_cpu(d.pop("max_total_cpu", UNSET))

        def _parse_max_total_memory_mb(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_total_memory_mb = _parse_max_total_memory_mb(
            d.pop("max_total_memory_mb", UNSET)
        )

        def _parse_min_machine_cpu(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        min_machine_cpu = _parse_min_machine_cpu(d.pop("min_machine_cpu", UNSET))

        def _parse_min_machine_memory_mb(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        min_machine_memory_mb = _parse_min_machine_memory_mb(
            d.pop("min_machine_memory_mb", UNSET)
        )

        def _parse_max_machine_cpu(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_machine_cpu = _parse_max_machine_cpu(d.pop("max_machine_cpu", UNSET))

        def _parse_max_machine_memory_mb(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_machine_memory_mb = _parse_max_machine_memory_mb(
            d.pop("max_machine_memory_mb", UNSET)
        )

        def _parse_delete_after_idle_minutes(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        delete_after_idle_minutes = _parse_delete_after_idle_minutes(
            d.pop("delete_after_idle_minutes", UNSET)
        )

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, MachineMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = MachineMetadata.from_dict(_metadata)

        update_machine_pool_request = cls(
            name=name,
            description=description,
            default_machine_cpu=default_machine_cpu,
            default_machine_memory_mb=default_machine_memory_mb,
            default_machine_env=default_machine_env,
            default_machine_secret_env=default_machine_secret_env,
            default_machine_provider_options=default_machine_provider_options,
            default_cwd=default_cwd,
            provider_config=provider_config,
            provider_auth_secret_id=provider_auth_secret_id,
            runtime_protection_enabled=runtime_protection_enabled,
            max_total_machines=max_total_machines,
            max_total_cpu=max_total_cpu,
            max_total_memory_mb=max_total_memory_mb,
            min_machine_cpu=min_machine_cpu,
            min_machine_memory_mb=min_machine_memory_mb,
            max_machine_cpu=max_machine_cpu,
            max_machine_memory_mb=max_machine_memory_mb,
            delete_after_idle_minutes=delete_after_idle_minutes,
            metadata=metadata,
        )

        return update_machine_pool_request
