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
    from ..models.check_machine_pool_connection_request_default_machine_provider_options import (
        CheckMachinePoolConnectionRequestDefaultMachineProviderOptions,
    )
    from ..models.check_machine_pool_connection_request_provider_config import (
        CheckMachinePoolConnectionRequestProviderConfig,
    )


T = TypeVar("T", bound="CheckMachinePoolConnectionRequest")


@_attrs_define
class CheckMachinePoolConnectionRequest:
    """
    Attributes:
        provider (str):
        provider_auth_secret_id (str): Secret ID (sec_...).
        provider_config (Union[Unset, CheckMachinePoolConnectionRequestProviderConfig]):
        default_machine_provider_options (Union[Unset, CheckMachinePoolConnectionRequestDefaultMachineProviderOptions]):
    """

    provider: str
    provider_auth_secret_id: str
    provider_config: Union[Unset, "CheckMachinePoolConnectionRequestProviderConfig"] = (
        UNSET
    )
    default_machine_provider_options: Union[
        Unset, "CheckMachinePoolConnectionRequestDefaultMachineProviderOptions"
    ] = UNSET

    def to_dict(self) -> dict[str, Any]:
        provider = self.provider

        provider_auth_secret_id = self.provider_auth_secret_id

        provider_config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.provider_config, Unset):
            provider_config = self.provider_config.to_dict()

        default_machine_provider_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.default_machine_provider_options, Unset):
            default_machine_provider_options = (
                self.default_machine_provider_options.to_dict()
            )

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "provider": provider,
                "provider_auth_secret_id": provider_auth_secret_id,
            }
        )
        if provider_config is not UNSET:
            field_dict["provider_config"] = provider_config
        if default_machine_provider_options is not UNSET:
            field_dict["default_machine_provider_options"] = (
                default_machine_provider_options
            )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.check_machine_pool_connection_request_default_machine_provider_options import (
            CheckMachinePoolConnectionRequestDefaultMachineProviderOptions,
        )
        from ..models.check_machine_pool_connection_request_provider_config import (
            CheckMachinePoolConnectionRequestProviderConfig,
        )

        d = dict(src_dict)
        provider = d.pop("provider")

        provider_auth_secret_id = d.pop("provider_auth_secret_id")

        _provider_config = d.pop("provider_config", UNSET)
        provider_config: Union[Unset, CheckMachinePoolConnectionRequestProviderConfig]
        if isinstance(_provider_config, Unset):
            provider_config = UNSET
        else:
            provider_config = CheckMachinePoolConnectionRequestProviderConfig.from_dict(
                _provider_config
            )

        _default_machine_provider_options = d.pop(
            "default_machine_provider_options", UNSET
        )
        default_machine_provider_options: Union[
            Unset, CheckMachinePoolConnectionRequestDefaultMachineProviderOptions
        ]
        if isinstance(_default_machine_provider_options, Unset):
            default_machine_provider_options = UNSET
        else:
            default_machine_provider_options = CheckMachinePoolConnectionRequestDefaultMachineProviderOptions.from_dict(
                _default_machine_provider_options
            )

        check_machine_pool_connection_request = cls(
            provider=provider,
            provider_auth_secret_id=provider_auth_secret_id,
            provider_config=provider_config,
            default_machine_provider_options=default_machine_provider_options,
        )

        return check_machine_pool_connection_request
