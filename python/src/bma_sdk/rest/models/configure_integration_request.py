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
    from ..models.integration_provider_config import IntegrationProviderConfig


T = TypeVar("T", bound="ConfigureIntegrationRequest")


@_attrs_define
class ConfigureIntegrationRequest:
    """Verifies credentials for this saved integration. GitHub tenant/account are the numeric App ID and Installation ID;
    the secret is github_app_credentials. Discord tenant is the Application ID; its generic secret contains the bot
    token, from which the bot User ID is discovered automatically. Reconnect preserves the original verified provider
    identity. A concurrent setup change rejects this request. Credential payloads are never returned.

        Attributes:
            expected_setup_revision (int):
            provider_tenant_id (str):
            credential_secret_id (str): Secret ID (sec_...).
            provider_account_ref (Union[Unset, str]): Required GitHub Installation ID. Optional for Discord; an explicitly
                supplied bot User ID must match the token.
            provider_agent_display_name (Union[Unset, str]): Provider account display label, at most 512 UTF-8 bytes.
                Leading and trailing whitespace is trimmed on save. Empty means no label; an omitted or empty value clears the
                label on account-management updates.
            provider_config (Union[Unset, IntegrationProviderConfig]): Non-secret provider configuration, validated for the
                selected provider. Slack and GitHub integrations require an empty object. Discord accepts only public_key
                (optional, a 32-byte hex-encoded Ed25519 verification key for interaction callbacks). BMA manages one Gateway
                connection per Discord integration. Credentials and integration behavior are not accepted here.
    """

    expected_setup_revision: int
    provider_tenant_id: str
    credential_secret_id: str
    provider_account_ref: Union[Unset, str] = UNSET
    provider_agent_display_name: Union[Unset, str] = UNSET
    provider_config: Union[Unset, "IntegrationProviderConfig"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        expected_setup_revision = self.expected_setup_revision

        provider_tenant_id = self.provider_tenant_id

        credential_secret_id = self.credential_secret_id

        provider_account_ref = self.provider_account_ref

        provider_agent_display_name = self.provider_agent_display_name

        provider_config: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.provider_config, Unset):
            provider_config = self.provider_config.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "expected_setup_revision": expected_setup_revision,
                "provider_tenant_id": provider_tenant_id,
                "credential_secret_id": credential_secret_id,
            }
        )
        if provider_account_ref is not UNSET:
            field_dict["provider_account_ref"] = provider_account_ref
        if provider_agent_display_name is not UNSET:
            field_dict["provider_agent_display_name"] = provider_agent_display_name
        if provider_config is not UNSET:
            field_dict["provider_config"] = provider_config

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_provider_config import IntegrationProviderConfig

        d = dict(src_dict)
        expected_setup_revision = d.pop("expected_setup_revision")

        provider_tenant_id = d.pop("provider_tenant_id")

        credential_secret_id = d.pop("credential_secret_id")

        provider_account_ref = d.pop("provider_account_ref", UNSET)

        provider_agent_display_name = d.pop("provider_agent_display_name", UNSET)

        _provider_config = d.pop("provider_config", UNSET)
        provider_config: Union[Unset, IntegrationProviderConfig]
        if isinstance(_provider_config, Unset):
            provider_config = UNSET
        else:
            provider_config = IntegrationProviderConfig.from_dict(_provider_config)

        configure_integration_request = cls(
            expected_setup_revision=expected_setup_revision,
            provider_tenant_id=provider_tenant_id,
            credential_secret_id=credential_secret_id,
            provider_account_ref=provider_account_ref,
            provider_agent_display_name=provider_agent_display_name,
            provider_config=provider_config,
        )

        return configure_integration_request
