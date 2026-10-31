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
    from ..models.connect_byo_machine_request_env import ConnectBYOMachineRequestEnv
    from ..models.connect_byo_machine_request_secret_env import (
        ConnectBYOMachineRequestSecretEnv,
    )
    from ..models.machine_metadata import MachineMetadata


T = TypeVar("T", bound="ConnectBYOMachineRequest")


@_attrs_define
class ConnectBYOMachineRequest:
    """
    Attributes:
        display_name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        description (Union[Unset, str]): Optional description of the machine.
        cwd (Union[Unset, str]): Default working directory for processes started on the machine.
        env (Union[Unset, ConnectBYOMachineRequestEnv]): Environment variables set for processes started on the machine.
        secret_env (Union[Unset, ConnectBYOMachineRequestSecretEnv]): Environment variable names mapped to secret IDs
            (sec_...) whose values are set for processes started on the machine.
        metadata (Union[Unset, MachineMetadata]): User-supplied metadata stored on a machine, provided directly or
            copied from the machine pool that provisions it. A restriction of Metadata that leaves room for one reserved
            pair - BMA sets observed_platform on the machine to the platform reported by its daemon, so the key is reserved
            and at most 15 user pairs are accepted.
        project_ids (Union[Unset, list[str]]): Projects to grant the machine to in the same call (up to 100).
        token_name (Union[Unset, str]): Human-readable name. Spaces and punctuation are allowed; leading or trailing
            whitespace and invisible or control characters are not.
    """

    display_name: str
    description: Union[Unset, str] = UNSET
    cwd: Union[Unset, str] = UNSET
    env: Union[Unset, "ConnectBYOMachineRequestEnv"] = UNSET
    secret_env: Union[Unset, "ConnectBYOMachineRequestSecretEnv"] = UNSET
    metadata: Union[Unset, "MachineMetadata"] = UNSET
    project_ids: Union[Unset, list[str]] = UNSET
    token_name: Union[Unset, str] = UNSET

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

        project_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.project_ids, Unset):
            project_ids = self.project_ids

        token_name = self.token_name

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
        if project_ids is not UNSET:
            field_dict["project_ids"] = project_ids
        if token_name is not UNSET:
            field_dict["token_name"] = token_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.connect_byo_machine_request_env import ConnectBYOMachineRequestEnv
        from ..models.connect_byo_machine_request_secret_env import (
            ConnectBYOMachineRequestSecretEnv,
        )
        from ..models.machine_metadata import MachineMetadata

        d = dict(src_dict)
        display_name = d.pop("display_name")

        description = d.pop("description", UNSET)

        cwd = d.pop("cwd", UNSET)

        _env = d.pop("env", UNSET)
        env: Union[Unset, ConnectBYOMachineRequestEnv]
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = ConnectBYOMachineRequestEnv.from_dict(_env)

        _secret_env = d.pop("secret_env", UNSET)
        secret_env: Union[Unset, ConnectBYOMachineRequestSecretEnv]
        if isinstance(_secret_env, Unset):
            secret_env = UNSET
        else:
            secret_env = ConnectBYOMachineRequestSecretEnv.from_dict(_secret_env)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, MachineMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = MachineMetadata.from_dict(_metadata)

        project_ids = cast(list[str], d.pop("project_ids", UNSET))

        token_name = d.pop("token_name", UNSET)

        connect_byo_machine_request = cls(
            display_name=display_name,
            description=description,
            cwd=cwd,
            env=env,
            secret_env=secret_env,
            metadata=metadata,
            project_ids=project_ids,
            token_name=token_name,
        )

        return connect_byo_machine_request
