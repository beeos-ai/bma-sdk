from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="ModelProviderConfigAuthOptions")


@_attrs_define
class ModelProviderConfigAuthOptions:
    """Non-secret authentication settings for this provider config.

    Attributes:
        header_name (Union[Unset, str]):
        service (Union[Unset, str]):
        region (Union[Unset, str]):
    """

    header_name: Union[Unset, str] = UNSET
    service: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        header_name = self.header_name

        service = self.service

        region = self.region

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if header_name is not UNSET:
            field_dict["header_name"] = header_name
        if service is not UNSET:
            field_dict["service"] = service
        if region is not UNSET:
            field_dict["region"] = region

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        header_name = d.pop("header_name", UNSET)

        service = d.pop("service", UNSET)

        region = d.pop("region", UNSET)

        model_provider_config_auth_options = cls(
            header_name=header_name,
            service=service,
            region=region,
        )

        return model_provider_config_auth_options
