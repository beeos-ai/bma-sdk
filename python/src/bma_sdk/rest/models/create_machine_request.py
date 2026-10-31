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
    from ..models.create_machine_request_env import CreateMachineRequestEnv
    from ..models.create_machine_request_secret_env import CreateMachineRequestSecretEnv
    from ..models.machine_metadata import MachineMetadata


T = TypeVar("T", bound="CreateMachineRequest")


@_attrs_define
class CreateMachineRequest:
    """
    Attributes:
        display_name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        description (Union[Unset, str]):
        cwd (Union[Unset, str]):
        env (Union[Unset, CreateMachineRequestEnv]):
        secret_env (Union[Unset, CreateMachineRequestSecretEnv]):
        metadata (Union[Unset, MachineMetadata]): User-supplied metadata stored on a machine, provided directly or
            copied from the machine pool that provisions it. A restriction of Metadata that leaves room for one reserved
            pair - BMA sets observed_platform on the machine to the platform reported by its daemon, so the key is reserved
            and at most 15 user pairs are accepted.
    """

    display_name: str
    description: Union[Unset, str] = UNSET
    cwd: Union[Unset, str] = UNSET
    env: Union[Unset, "CreateMachineRequestEnv"] = UNSET
    secret_env: Union[Unset, "CreateMachineRequestSecretEnv"] = UNSET
    metadata: Union[Unset, "MachineMetadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        description = self.description

        cwd = self.cwd

        env: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.env, Unset):
            env = self.env.to_dict()

        secret_env: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.secret_env, Unset):
            secret_env = self.secret_env.to_dict()

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "display_name": display_name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if cwd is not UNSET:
            field_dict["cwd"] = cwd
        if env is not UNSET:
            field_dict["env"] = env
        if secret_env is not UNSET:
            field_dict["secret_env"] = secret_env
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_machine_request_env import CreateMachineRequestEnv
        from ..models.create_machine_request_secret_env import (
            CreateMachineRequestSecretEnv,
        )
        from ..models.machine_metadata import MachineMetadata

        d = dict(src_dict)
        display_name = d.pop("display_name")

        description = d.pop("description", UNSET)

        cwd = d.pop("cwd", UNSET)

        _env = d.pop("env", UNSET)
        env: Union[Unset, CreateMachineRequestEnv]
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = CreateMachineRequestEnv.from_dict(_env)

        _secret_env = d.pop("secret_env", UNSET)
        secret_env: Union[Unset, CreateMachineRequestSecretEnv]
        if isinstance(_secret_env, Unset):
            secret_env = UNSET
        else:
            secret_env = CreateMachineRequestSecretEnv.from_dict(_secret_env)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, MachineMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = MachineMetadata.from_dict(_metadata)

        create_machine_request = cls(
            display_name=display_name,
            description=description,
            cwd=cwd,
            env=env,
            secret_env=secret_env,
            metadata=metadata,
        )

        return create_machine_request
