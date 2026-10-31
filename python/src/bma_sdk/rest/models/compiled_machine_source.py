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
    from ..models.compiled_machine_source_env_overlay import (
        CompiledMachineSourceEnvOverlay,
    )
    from ..models.compiled_machine_source_machine_provider_options_overlay import (
        CompiledMachineSourceMachineProviderOptionsOverlay,
    )
    from ..models.compiled_machine_source_secret_env_overlay import (
        CompiledMachineSourceSecretEnvOverlay,
    )


T = TypeVar("T", bound="CompiledMachineSource")


@_attrs_define
class CompiledMachineSource:
    """
    Attributes:
        machine_id (Union[Unset, str]): Machine ID (mch_...).
        machine_pool_id (Union[Unset, str]): Machine pool ID (mpo_...).
        max_machines (Union[Unset, int]):
        initial_num_machines (Union[Unset, int]):
        delete_after_idle_minutes (Union[Unset, int]):
        cwd (Union[Unset, str]):
        machine_cpu (Union[Unset, int]):
        machine_memory_mb (Union[Unset, int]):
        env_overlay (Union[Unset, CompiledMachineSourceEnvOverlay]):
        secret_env_overlay (Union[Unset, CompiledMachineSourceSecretEnvOverlay]):
        machine_provider_options_overlay (Union[Unset, CompiledMachineSourceMachineProviderOptionsOverlay]):
        description (Union[Unset, str]):
    """

    machine_id: Union[Unset, str] = UNSET
    machine_pool_id: Union[Unset, str] = UNSET
    max_machines: Union[Unset, int] = UNSET
    initial_num_machines: Union[Unset, int] = UNSET
    delete_after_idle_minutes: Union[Unset, int] = UNSET
    cwd: Union[Unset, str] = UNSET
    machine_cpu: Union[Unset, int] = UNSET
    machine_memory_mb: Union[Unset, int] = UNSET
    env_overlay: Union[Unset, "CompiledMachineSourceEnvOverlay"] = UNSET
    secret_env_overlay: Union[Unset, "CompiledMachineSourceSecretEnvOverlay"] = UNSET
    machine_provider_options_overlay: Union[
        Unset, "CompiledMachineSourceMachineProviderOptionsOverlay"
    ] = UNSET
    description: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        machine_id = self.machine_id

        machine_pool_id = self.machine_pool_id

        max_machines = self.max_machines

        initial_num_machines = self.initial_num_machines

        delete_after_idle_minutes = self.delete_after_idle_minutes

        cwd = self.cwd

        machine_cpu = self.machine_cpu

        machine_memory_mb = self.machine_memory_mb

        env_overlay: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.env_overlay, Unset):
            env_overlay = self.env_overlay.to_dict()

        secret_env_overlay: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.secret_env_overlay, Unset):
            secret_env_overlay = self.secret_env_overlay.to_dict()

        machine_provider_options_overlay: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.machine_provider_options_overlay, Unset):
            machine_provider_options_overlay = (
                self.machine_provider_options_overlay.to_dict()
            )

        description = self.description

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if machine_id is not UNSET:
            field_dict["machine_id"] = machine_id
        if machine_pool_id is not UNSET:
            field_dict["machine_pool_id"] = machine_pool_id
        if max_machines is not UNSET:
            field_dict["max_machines"] = max_machines
        if initial_num_machines is not UNSET:
            field_dict["initial_num_machines"] = initial_num_machines
        if delete_after_idle_minutes is not UNSET:
            field_dict["delete_after_idle_minutes"] = delete_after_idle_minutes
        if cwd is not UNSET:
            field_dict["cwd"] = cwd
        if machine_cpu is not UNSET:
            field_dict["machine_cpu"] = machine_cpu
        if machine_memory_mb is not UNSET:
            field_dict["machine_memory_mb"] = machine_memory_mb
        if env_overlay is not UNSET:
            field_dict["env_overlay"] = env_overlay
        if secret_env_overlay is not UNSET:
            field_dict["secret_env_overlay"] = secret_env_overlay
        if machine_provider_options_overlay is not UNSET:
            field_dict["machine_provider_options_overlay"] = (
                machine_provider_options_overlay
            )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.compiled_machine_source_env_overlay import (
            CompiledMachineSourceEnvOverlay,
        )
        from ..models.compiled_machine_source_machine_provider_options_overlay import (
            CompiledMachineSourceMachineProviderOptionsOverlay,
        )
        from ..models.compiled_machine_source_secret_env_overlay import (
            CompiledMachineSourceSecretEnvOverlay,
        )

        d = dict(src_dict)
        machine_id = d.pop("machine_id", UNSET)

        machine_pool_id = d.pop("machine_pool_id", UNSET)

        max_machines = d.pop("max_machines", UNSET)

        initial_num_machines = d.pop("initial_num_machines", UNSET)

        delete_after_idle_minutes = d.pop("delete_after_idle_minutes", UNSET)

        cwd = d.pop("cwd", UNSET)

        machine_cpu = d.pop("machine_cpu", UNSET)

        machine_memory_mb = d.pop("machine_memory_mb", UNSET)

        _env_overlay = d.pop("env_overlay", UNSET)
        env_overlay: Union[Unset, CompiledMachineSourceEnvOverlay]
        if isinstance(_env_overlay, Unset):
            env_overlay = UNSET
        else:
            env_overlay = CompiledMachineSourceEnvOverlay.from_dict(_env_overlay)

        _secret_env_overlay = d.pop("secret_env_overlay", UNSET)
        secret_env_overlay: Union[Unset, CompiledMachineSourceSecretEnvOverlay]
        if isinstance(_secret_env_overlay, Unset):
            secret_env_overlay = UNSET
        else:
            secret_env_overlay = CompiledMachineSourceSecretEnvOverlay.from_dict(
                _secret_env_overlay
            )

        _machine_provider_options_overlay = d.pop(
            "machine_provider_options_overlay", UNSET
        )
        machine_provider_options_overlay: Union[
            Unset, CompiledMachineSourceMachineProviderOptionsOverlay
        ]
        if isinstance(_machine_provider_options_overlay, Unset):
            machine_provider_options_overlay = UNSET
        else:
            machine_provider_options_overlay = (
                CompiledMachineSourceMachineProviderOptionsOverlay.from_dict(
                    _machine_provider_options_overlay
                )
            )

        description = d.pop("description", UNSET)

        compiled_machine_source = cls(
            machine_id=machine_id,
            machine_pool_id=machine_pool_id,
            max_machines=max_machines,
            initial_num_machines=initial_num_machines,
            delete_after_idle_minutes=delete_after_idle_minutes,
            cwd=cwd,
            machine_cpu=machine_cpu,
            machine_memory_mb=machine_memory_mb,
            env_overlay=env_overlay,
            secret_env_overlay=secret_env_overlay,
            machine_provider_options_overlay=machine_provider_options_overlay,
            description=description,
        )

        return compiled_machine_source
