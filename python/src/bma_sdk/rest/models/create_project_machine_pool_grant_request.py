from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_project_machine_pool_grant_request_default_machine_env_overlay import (
        CreateProjectMachinePoolGrantRequestDefaultMachineEnvOverlay,
    )
    from ..models.create_project_machine_pool_grant_request_default_machine_provider_options_overlay import (
        CreateProjectMachinePoolGrantRequestDefaultMachineProviderOptionsOverlay,
    )
    from ..models.create_project_machine_pool_grant_request_default_machine_secret_env_overlay import (
        CreateProjectMachinePoolGrantRequestDefaultMachineSecretEnvOverlay,
    )
    from ..models.metadata import Metadata


T = TypeVar("T", bound="CreateProjectMachinePoolGrantRequest")


@_attrs_define
class CreateProjectMachinePoolGrantRequest:
    """
    Attributes:
        machine_pool_id (str): Machine pool ID (mpo_...).
        description (Union[Unset, str]): Optional note about this grant.
        default_machine_cpu (Union[Unset, int]): Default CPU count for machines this project creates from the pool,
            overriding the pool's default.
        default_machine_memory_mb (Union[Unset, int]): Default memory in MB for machines this project creates from the
            pool, overriding the pool's default.
        default_machine_env_overlay (Union[Unset, CreateProjectMachinePoolGrantRequestDefaultMachineEnvOverlay]): Env
            overlay merged over the pool's default_machine_env for machines materialized through this grant; a null entry
            removes the key.
        default_machine_secret_env_overlay (Union[Unset,
            CreateProjectMachinePoolGrantRequestDefaultMachineSecretEnvOverlay]): Secret env overlay merged over the pool's
            default_machine_secret_env for machines materialized through this grant; a null entry removes the key.
        default_machine_provider_options_overlay (Union[Unset,
            CreateProjectMachinePoolGrantRequestDefaultMachineProviderOptionsOverlay]): Provider-specific options layered
            over the pool's provider options for this project's machines.
        default_cwd (Union[Unset, str]): Default working directory for processes on this project's machines from the
            pool.
        max_total_machines (Union[Unset, int]): Maximum number of live machines this project can have from the pool.
        max_total_cpu (Union[Unset, int]): Maximum total CPU across this project's live machines from the pool.
        max_total_memory_mb (Union[Unset, int]): Maximum total memory in MB across this project's live machines from the
            pool.
        min_machine_cpu (Union[Unset, int]): Smallest CPU count one of this project's machines can request.
        min_machine_memory_mb (Union[Unset, int]): Smallest memory in MB one of this project's machines can request.
        max_machine_cpu (Union[Unset, int]): Largest CPU count one of this project's machines can request.
        max_machine_memory_mb (Union[Unset, int]): Largest memory in MB one of this project's machines can request.
        delete_after_idle_minutes (Union[Literal[0], Unset, int]): Idle minutes before deleting a machine created
            through this grant. Use 0 to disable for this grant; omit to inherit the pool default. Values from 1 through 4
            are invalid.
        metadata (Union[Unset, Metadata]): Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64 characters,
            values must be strings of up to 512 characters.
    """

    machine_pool_id: str
    description: Union[Unset, str] = UNSET
    default_machine_cpu: Union[Unset, int] = UNSET
    default_machine_memory_mb: Union[Unset, int] = UNSET
    default_machine_env_overlay: Union[
        Unset, "CreateProjectMachinePoolGrantRequestDefaultMachineEnvOverlay"
    ] = UNSET
    default_machine_secret_env_overlay: Union[
        Unset, "CreateProjectMachinePoolGrantRequestDefaultMachineSecretEnvOverlay"
    ] = UNSET
    default_machine_provider_options_overlay: Union[
        Unset,
        "CreateProjectMachinePoolGrantRequestDefaultMachineProviderOptionsOverlay",
    ] = UNSET
    default_cwd: Union[Unset, str] = UNSET
    max_total_machines: Union[Unset, int] = UNSET
    max_total_cpu: Union[Unset, int] = UNSET
    max_total_memory_mb: Union[Unset, int] = UNSET
    min_machine_cpu: Union[Unset, int] = UNSET
    min_machine_memory_mb: Union[Unset, int] = UNSET
    max_machine_cpu: Union[Unset, int] = UNSET
    max_machine_memory_mb: Union[Unset, int] = UNSET
    delete_after_idle_minutes: Union[Literal[0], Unset, int] = UNSET
    metadata: Union[Unset, "Metadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        machine_pool_id = self.machine_pool_id

        description = self.description

        default_machine_cpu = self.default_machine_cpu

        default_machine_memory_mb = self.default_machine_memory_mb

        default_machine_env_overlay: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.default_machine_env_overlay, Unset):
            default_machine_env_overlay = self.default_machine_env_overlay.to_dict()

        default_machine_secret_env_overlay: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.default_machine_secret_env_overlay, Unset):
            default_machine_secret_env_overlay = (
                self.default_machine_secret_env_overlay.to_dict()
            )

        default_machine_provider_options_overlay: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.default_machine_provider_options_overlay, Unset):
            default_machine_provider_options_overlay = (
                self.default_machine_provider_options_overlay.to_dict()
            )

        default_cwd = self.default_cwd

        max_total_machines = self.max_total_machines

        max_total_cpu = self.max_total_cpu

        max_total_memory_mb = self.max_total_memory_mb

        min_machine_cpu = self.min_machine_cpu

        min_machine_memory_mb = self.min_machine_memory_mb

        max_machine_cpu = self.max_machine_cpu

        max_machine_memory_mb = self.max_machine_memory_mb

        delete_after_idle_minutes: Union[Literal[0], Unset, int]
        if isinstance(self.delete_after_idle_minutes, Unset):
            delete_after_idle_minutes = UNSET
        else:
            delete_after_idle_minutes = self.delete_after_idle_minutes

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "machine_pool_id": machine_pool_id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if default_machine_cpu is not UNSET:
            field_dict["default_machine_cpu"] = default_machine_cpu
        if default_machine_memory_mb is not UNSET:
            field_dict["default_machine_memory_mb"] = default_machine_memory_mb
        if default_machine_env_overlay is not UNSET:
            field_dict["default_machine_env_overlay"] = default_machine_env_overlay
        if default_machine_secret_env_overlay is not UNSET:
            field_dict["default_machine_secret_env_overlay"] = (
                default_machine_secret_env_overlay
            )
        if default_machine_provider_options_overlay is not UNSET:
            field_dict["default_machine_provider_options_overlay"] = (
                default_machine_provider_options_overlay
            )
        if default_cwd is not UNSET:
            field_dict["default_cwd"] = default_cwd
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
        from ..models.create_project_machine_pool_grant_request_default_machine_env_overlay import (
            CreateProjectMachinePoolGrantRequestDefaultMachineEnvOverlay,
        )
        from ..models.create_project_machine_pool_grant_request_default_machine_provider_options_overlay import (
            CreateProjectMachinePoolGrantRequestDefaultMachineProviderOptionsOverlay,
        )
        from ..models.create_project_machine_pool_grant_request_default_machine_secret_env_overlay import (
            CreateProjectMachinePoolGrantRequestDefaultMachineSecretEnvOverlay,
        )
        from ..models.metadata import Metadata

        d = dict(src_dict)
        machine_pool_id = d.pop("machine_pool_id")

        description = d.pop("description", UNSET)

        default_machine_cpu = d.pop("default_machine_cpu", UNSET)

        default_machine_memory_mb = d.pop("default_machine_memory_mb", UNSET)

        _default_machine_env_overlay = d.pop("default_machine_env_overlay", UNSET)
        default_machine_env_overlay: Union[
            Unset, CreateProjectMachinePoolGrantRequestDefaultMachineEnvOverlay
        ]
        if isinstance(_default_machine_env_overlay, Unset):
            default_machine_env_overlay = UNSET
        else:
            default_machine_env_overlay = (
                CreateProjectMachinePoolGrantRequestDefaultMachineEnvOverlay.from_dict(
                    _default_machine_env_overlay
                )
            )

        _default_machine_secret_env_overlay = d.pop(
            "default_machine_secret_env_overlay", UNSET
        )
        default_machine_secret_env_overlay: Union[
            Unset, CreateProjectMachinePoolGrantRequestDefaultMachineSecretEnvOverlay
        ]
        if isinstance(_default_machine_secret_env_overlay, Unset):
            default_machine_secret_env_overlay = UNSET
        else:
            default_machine_secret_env_overlay = CreateProjectMachinePoolGrantRequestDefaultMachineSecretEnvOverlay.from_dict(
                _default_machine_secret_env_overlay
            )

        _default_machine_provider_options_overlay = d.pop(
            "default_machine_provider_options_overlay", UNSET
        )
        default_machine_provider_options_overlay: Union[
            Unset,
            CreateProjectMachinePoolGrantRequestDefaultMachineProviderOptionsOverlay,
        ]
        if isinstance(_default_machine_provider_options_overlay, Unset):
            default_machine_provider_options_overlay = UNSET
        else:
            default_machine_provider_options_overlay = CreateProjectMachinePoolGrantRequestDefaultMachineProviderOptionsOverlay.from_dict(
                _default_machine_provider_options_overlay
            )

        default_cwd = d.pop("default_cwd", UNSET)

        max_total_machines = d.pop("max_total_machines", UNSET)

        max_total_cpu = d.pop("max_total_cpu", UNSET)

        max_total_memory_mb = d.pop("max_total_memory_mb", UNSET)

        min_machine_cpu = d.pop("min_machine_cpu", UNSET)

        min_machine_memory_mb = d.pop("min_machine_memory_mb", UNSET)

        max_machine_cpu = d.pop("max_machine_cpu", UNSET)

        max_machine_memory_mb = d.pop("max_machine_memory_mb", UNSET)

        def _parse_delete_after_idle_minutes(
            data: object,
        ) -> Union[Literal[0], Unset, int]:
            if isinstance(data, Unset):
                return data
            delete_after_idle_minutes_type_0 = cast(Literal[0], data)
            if delete_after_idle_minutes_type_0 != 0:
                raise ValueError(
                    f"delete_after_idle_minutes_type_0 must match const 0, got '{delete_after_idle_minutes_type_0}'"
                )
            return delete_after_idle_minutes_type_0
            return cast(Union[Literal[0], Unset, int], data)

        delete_after_idle_minutes = _parse_delete_after_idle_minutes(
            d.pop("delete_after_idle_minutes", UNSET)
        )

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, Metadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = Metadata.from_dict(_metadata)

        create_project_machine_pool_grant_request = cls(
            machine_pool_id=machine_pool_id,
            description=description,
            default_machine_cpu=default_machine_cpu,
            default_machine_memory_mb=default_machine_memory_mb,
            default_machine_env_overlay=default_machine_env_overlay,
            default_machine_secret_env_overlay=default_machine_secret_env_overlay,
            default_machine_provider_options_overlay=default_machine_provider_options_overlay,
            default_cwd=default_cwd,
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

        return create_project_machine_pool_grant_request
