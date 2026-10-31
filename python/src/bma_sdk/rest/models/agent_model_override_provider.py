from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.agent_model_override_provider_api_format import (
    AgentModelOverrideProviderApiFormat,
    check_agent_model_override_provider_api_format,
)
from ..models.agent_model_override_provider_api_variant import (
    AgentModelOverrideProviderApiVariant,
    check_agent_model_override_provider_api_variant,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentModelOverrideProvider")


@_attrs_define
class AgentModelOverrideProvider:
    """
    Attributes:
        api_format (AgentModelOverrideProviderApiFormat):
        base_url (str): HTTPS origin only; must not contain userinfo, query, fragment or a trailing slash. Private and
            link-local hosts are rejected by provider validation.
        api_variant (Union[Unset, AgentModelOverrideProviderApiVariant]):  Default: 'default'.
        endpoint_path (Union[Unset, str]):  Default: '/v1/chat/completions'.
    """

    api_format: AgentModelOverrideProviderApiFormat
    base_url: str
    api_variant: Union[Unset, AgentModelOverrideProviderApiVariant] = "default"
    endpoint_path: Union[Unset, str] = "/v1/chat/completions"

    def to_dict(self) -> dict[str, Any]:
        api_format: str = self.api_format

        base_url = self.base_url

        api_variant: Union[Unset, str] = UNSET
        if not isinstance(self.api_variant, Unset):
            api_variant = self.api_variant

        endpoint_path = self.endpoint_path

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "api_format": api_format,
                "base_url": base_url,
            }
        )
        if api_variant is not UNSET:
            field_dict["api_variant"] = api_variant
        if endpoint_path is not UNSET:
            field_dict["endpoint_path"] = endpoint_path

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        api_format = check_agent_model_override_provider_api_format(d.pop("api_format"))

        base_url = d.pop("base_url")

        _api_variant = d.pop("api_variant", UNSET)
        api_variant: Union[Unset, AgentModelOverrideProviderApiVariant]
        if isinstance(_api_variant, Unset):
            api_variant = UNSET
        else:
            api_variant = check_agent_model_override_provider_api_variant(_api_variant)

        endpoint_path = d.pop("endpoint_path", UNSET)

        agent_model_override_provider = cls(
            api_format=api_format,
            base_url=base_url,
            api_variant=api_variant,
            endpoint_path=endpoint_path,
        )

        return agent_model_override_provider
