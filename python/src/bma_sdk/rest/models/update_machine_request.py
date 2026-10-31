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
    from ..models.update_machine_request_env import UpdateMachineRequestEnv
    from ..models.update_machine_request_secret_env import UpdateMachineRequestSecretEnv


T = TypeVar("T", bound="UpdateMachineRequest")


@_attrs_define
class UpdateMachineRequest:
    """
    Attributes:
        cwd (Union[Unset, str]): Default working directory for processes started on the machine.
        env (Union[Unset, UpdateMachineRequestEnv]): Environment variables set for processes started on the machine.
        secret_env (Union[Unset, UpdateMachineRequestSecretEnv]): Environment variable names mapped to secret IDs
            (sec_...) whose values are set for processes started on the machine.
    """

    cwd: Union[Unset, str] = UNSET
    env: Union[Unset, "UpdateMachineRequestEnv"] = UNSET
    secret_env: Union[Unset, "UpdateMachineRequestSecretEnv"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        cwd = self.cwd

        env: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.env, Unset):
            env = self.env.to_dict()

        secret_env: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.secret_env, Unset):
            secret_env = self.secret_env.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if cwd is not UNSET:
            field_dict["cwd"] = cwd
        if env is not UNSET:
            field_dict["env"] = env
        if secret_env is not UNSET:
            field_dict["secret_env"] = secret_env

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_machine_request_env import UpdateMachineRequestEnv
        from ..models.update_machine_request_secret_env import (
            UpdateMachineRequestSecretEnv,
        )

        d = dict(src_dict)
        cwd = d.pop("cwd", UNSET)

        _env = d.pop("env", UNSET)
        env: Union[Unset, UpdateMachineRequestEnv]
        if isinstance(_env, Unset):
            env = UNSET
        else:
            env = UpdateMachineRequestEnv.from_dict(_env)

        _secret_env = d.pop("secret_env", UNSET)
        secret_env: Union[Unset, UpdateMachineRequestSecretEnv]
        if isinstance(_secret_env, Unset):
            secret_env = UNSET
        else:
            secret_env = UpdateMachineRequestSecretEnv.from_dict(_secret_env)

        update_machine_request = cls(
            cwd=cwd,
            env=env,
            secret_env=secret_env,
        )

        return update_machine_request
