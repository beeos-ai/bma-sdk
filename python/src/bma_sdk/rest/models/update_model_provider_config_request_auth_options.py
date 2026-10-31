from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateModelProviderConfigRequestAuthOptions")


@_attrs_define
class UpdateModelProviderConfigRequestAuthOptions:
    """Non-secret authentication settings. Use an empty object with bearer_token. With api_key_header, set
    {"header_name":"..."}. With sigv4, set the AWS signing service and region.

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

        update_model_provider_config_request_auth_options = cls(
            header_name=header_name,
            service=service,
            region=region,
        )

        return update_model_provider_config_request_auth_options
