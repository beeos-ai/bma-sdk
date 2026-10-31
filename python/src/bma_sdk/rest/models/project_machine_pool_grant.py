import datetime
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
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.metadata import Metadata
    from ..models.project_machine_pool_grant_default_machine_env_overlay import (
        ProjectMachinePoolGrantDefaultMachineEnvOverlay,
    )
    from ..models.project_machine_pool_grant_default_machine_provider_options_overlay import (
        ProjectMachinePoolGrantDefaultMachineProviderOptionsOverlay,
    )
    from ..models.project_machine_pool_grant_default_machine_secret_env_overlay import (
        ProjectMachinePoolGrantDefaultMachineSecretEnvOverlay,
    )


T = TypeVar("T", bound="ProjectMachinePoolGrant")


@_attrs_define
class ProjectMachinePoolGrant:
    """
    Attributes:
        id (str):
        org_id (str):
        project_id (str): Project ID (proj_...).
        machine_pool_id (str): Machine pool ID (mpo_...).
        description (str):
        default_machine_cpu (Union[None, int]):
        default_machine_memory_mb (Union[None, int]):
        default_machine_env_overlay (ProjectMachinePoolGrantDefaultMachineEnvOverlay): Env overlay merged over the
            pool's default_machine_env for machines materialized through this grant; a null entry removes the key.
        default_machine_secret_env_overlay (ProjectMachinePoolGrantDefaultMachineSecretEnvOverlay): Secret env overlay
            merged over the pool's default_machine_secret_env for machines materialized through this grant; a null entry
            removes the key.
        default_machine_provider_options_overlay (ProjectMachinePoolGrantDefaultMachineProviderOptionsOverlay):
        default_cwd (str):
        max_total_machines (Union[None, int]):
        max_total_cpu (Union[None, int]):
        max_total_memory_mb (Union[None, int]):
        min_machine_cpu (Union[None, int]):
        min_machine_memory_mb (Union[None, int]):
        max_machine_cpu (Union[None, int]):
        max_machine_memory_mb (Union[None, int]):
        delete_after_idle_minutes (Union[Literal[0], None, int]): Idle minutes before deleting a machine created through
            this grant. Zero disables deletion for this grant; null inherits the pool default.
        metadata (Metadata): Arbitrary key-value metadata. Maximum 16 pairs, keys up to 64 characters, values must be
            strings of up to 512 characters.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: str
    org_id: str
    project_id: str
    machine_pool_id: str
    description: str
    default_machine_cpu: Union[None, int]
    default_machine_memory_mb: Union[None, int]
    default_machine_env_overlay: "ProjectMachinePoolGrantDefaultMachineEnvOverlay"
    default_machine_secret_env_overlay: (
        "ProjectMachinePoolGrantDefaultMachineSecretEnvOverlay"
    )
    default_machine_provider_options_overlay: (
        "ProjectMachinePoolGrantDefaultMachineProviderOptionsOverlay"
    )
    default_cwd: str
    max_total_machines: Union[None, int]
    max_total_cpu: Union[None, int]
    max_total_memory_mb: Union[None, int]
    min_machine_cpu: Union[None, int]
    min_machine_memory_mb: Union[None, int]
    max_machine_cpu: Union[None, int]
    max_machine_memory_mb: Union[None, int]
    delete_after_idle_minutes: Union[Literal[0], None, int]
    metadata: "Metadata"
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        machine_pool_id = self.machine_pool_id

        description = self.description

        default_machine_cpu: Union[None, int]
        default_machine_cpu = self.default_machine_cpu

        default_machine_memory_mb: Union[None, int]
        default_machine_memory_mb = self.default_machine_memory_mb

        default_machine_env_overlay = self.default_machine_env_overlay.to_dict()

        default_machine_secret_env_overlay = (
            self.default_machine_secret_env_overlay.to_dict()
        )

        default_machine_provider_options_overlay = (
            self.default_machine_provider_options_overlay.to_dict()
        )

        default_cwd = self.default_cwd

        max_total_machines: Union[None, int]
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

        delete_after_idle_minutes: Union[Literal[0], None, int]
        delete_after_idle_minutes = self.delete_after_idle_minutes

        metadata = self.metadata.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "machine_pool_id": machine_pool_id,
                "description": description,
                "default_machine_cpu": default_machine_cpu,
                "default_machine_memory_mb": default_machine_memory_mb,
                "default_machine_env_overlay": default_machine_env_overlay,
                "default_machine_secret_env_overlay": default_machine_secret_env_overlay,
                "default_machine_provider_options_overlay": default_machine_provider_options_overlay,
                "default_cwd": default_cwd,
                "max_total_machines": max_total_machines,
                "max_total_cpu": max_total_cpu,
                "max_total_memory_mb": max_total_memory_mb,
                "min_machine_cpu": min_machine_cpu,
                "min_machine_memory_mb": min_machine_memory_mb,
                "max_machine_cpu": max_machine_cpu,
                "max_machine_memory_mb": max_machine_memory_mb,
                "delete_after_idle_minutes": delete_after_idle_minutes,
                "metadata": metadata,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata import Metadata
        from ..models.project_machine_pool_grant_default_machine_env_overlay import (
            ProjectMachinePoolGrantDefaultMachineEnvOverlay,
        )
        from ..models.project_machine_pool_grant_default_machine_provider_options_overlay import (
            ProjectMachinePoolGrantDefaultMachineProviderOptionsOverlay,
        )
        from ..models.project_machine_pool_grant_default_machine_secret_env_overlay import (
            ProjectMachinePoolGrantDefaultMachineSecretEnvOverlay,
        )

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        machine_pool_id = d.pop("machine_pool_id")

        description = d.pop("description")

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

        default_machine_env_overlay = (
            ProjectMachinePoolGrantDefaultMachineEnvOverlay.from_dict(
                d.pop("default_machine_env_overlay")
            )
        )

        default_machine_secret_env_overlay = (
            ProjectMachinePoolGrantDefaultMachineSecretEnvOverlay.from_dict(
                d.pop("default_machine_secret_env_overlay")
            )
        )

        default_machine_provider_options_overlay = (
            ProjectMachinePoolGrantDefaultMachineProviderOptionsOverlay.from_dict(
                d.pop("default_machine_provider_options_overlay")
            )
        )

        default_cwd = d.pop("default_cwd")

        def _parse_max_total_machines(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_total_machines = _parse_max_total_machines(d.pop("max_total_machines"))

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

        def _parse_delete_after_idle_minutes(
            data: object,
        ) -> Union[Literal[0], None, int]:
            if data is None:
                return data
            delete_after_idle_minutes_type_0 = cast(Literal[0], data)
            if delete_after_idle_minutes_type_0 != 0:
                raise ValueError(
                    f"delete_after_idle_minutes_type_0 must match const 0, got '{delete_after_idle_minutes_type_0}'"
                )
            return delete_after_idle_minutes_type_0
            delete_after_idle_minutes_type_3_type_0 = cast(Literal[0], data)
            if delete_after_idle_minutes_type_3_type_0 != 0:
                raise ValueError(
                    f"delete_after_idle_minutes_type_3_type_0 must match const 0, got '{delete_after_idle_minutes_type_3_type_0}'"
                )
            return delete_after_idle_minutes_type_3_type_0
            delete_after_idle_minutes_type_4_type_0 = cast(Literal[0], data)
            if delete_after_idle_minutes_type_4_type_0 != 0:
                raise ValueError(
                    f"delete_after_idle_minutes_type_4_type_0 must match const 0, got '{delete_after_idle_minutes_type_4_type_0}'"
                )
            return delete_after_idle_minutes_type_4_type_0
            return cast(Union[Literal[0], None, int], data)

        delete_after_idle_minutes = _parse_delete_after_idle_minutes(
            d.pop("delete_after_idle_minutes")
        )

        metadata = Metadata.from_dict(d.pop("metadata"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        project_machine_pool_grant = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
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
            created_at=created_at,
            updated_at=updated_at,
        )

        return project_machine_pool_grant
