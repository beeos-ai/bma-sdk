import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.integration_kind import IntegrationKind, check_integration_kind
from ..models.integration_state import IntegrationState, check_integration_state
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.integration_capabilities import IntegrationCapabilities
    from ..models.integration_provider_config import IntegrationProviderConfig
    from ..models.integration_runtime_failure import IntegrationRuntimeFailure
    from ..models.integration_settings import IntegrationSettings


T = TypeVar("T", bound="Integration")


@_attrs_define
class Integration:
    """
    Attributes:
        id (str):
        project_id (str): Project ID (proj_...).
        name (str): Immutable, project-unique integration name used in config keys and qualified tool names.
        integration_kind (IntegrationKind): Registered integration implementation; independent of the saved
            integration's name and immutable ID.
        state (IntegrationState):
        setup_revision (int): Credential and transport revision. Launcher edits leave this value unchanged.
        settings (IntegrationSettings): Integration-owned settings JSON. Validate against
            capabilities.settings.input_schema from the integration catalog. Public profile references use aprf_ IDs and
            resolve at runtime. GitHub integrations use GitHubIntegrationSettings; Slack and Discord integrations use
            ChatIntegrationSettings.
        provider_agent_display_name (str): Provider account display label, at most 512 UTF-8 bytes. Leading and trailing
            whitespace is trimmed on save. Empty means no label; an omitted or empty value clears the label on account-
            management updates.
        provider_config (IntegrationProviderConfig): Non-secret provider configuration, validated for the selected
            provider. Slack and GitHub integrations require an empty object. Discord accepts only public_key (optional, a
            32-byte hex-encoded Ed25519 verification key for interaction callbacks). BMA manages one Gateway connection per
            Discord integration. Credentials and integration behavior are not accepted here.
        capabilities (IntegrationCapabilities):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        last_oauth_flow_id (Union[Unset, str]):
        runtime_failure (Union[Unset, IntegrationRuntimeFailure]): Most recent connection failure for the active
            integration's current setup and credential version. Returned only by Get integration, not list or mutation
            responses. Omission does not establish provider connectivity; a runtime lease is not a connection check.
        provider_tenant_id (Union[Unset, str]): Verified provider identity, omitted until first connection. Retained
            after disconnect.
        provider_account_ref (Union[Unset, str]): Verified provider account, omitted until first connection. Retained
            after disconnect.
        bot_mention (Union[Unset, str]): GitHub App mention including the leading @, derived from the verified App slug.
            Omitted when the verified slug is unavailable or the integration is not GitHub. Retained after disconnect.
        credential_secret_id (Union[Unset, str]): Secret ID (sec_...).
    """

    id: str
    project_id: str
    name: str
    integration_kind: IntegrationKind
    state: IntegrationState
    setup_revision: int
    settings: "IntegrationSettings"
    provider_agent_display_name: str
    provider_config: "IntegrationProviderConfig"
    capabilities: "IntegrationCapabilities"
    created_at: datetime.datetime
    updated_at: datetime.datetime
    last_oauth_flow_id: Union[Unset, str] = UNSET
    runtime_failure: Union[Unset, "IntegrationRuntimeFailure"] = UNSET
    provider_tenant_id: Union[Unset, str] = UNSET
    provider_account_ref: Union[Unset, str] = UNSET
    bot_mention: Union[Unset, str] = UNSET
    credential_secret_id: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        project_id = self.project_id

        name = self.name

        integration_kind: str = self.integration_kind

        state: str = self.state

        setup_revision = self.setup_revision

        settings = self.settings.to_dict()

        provider_agent_display_name = self.provider_agent_display_name

        provider_config = self.provider_config.to_dict()

        capabilities = self.capabilities.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        last_oauth_flow_id = self.last_oauth_flow_id

        runtime_failure: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.runtime_failure, Unset):
            runtime_failure = self.runtime_failure.to_dict()

        provider_tenant_id = self.provider_tenant_id

        provider_account_ref = self.provider_account_ref

        bot_mention = self.bot_mention

        credential_secret_id = self.credential_secret_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "project_id": project_id,
                "name": name,
                "integration_kind": integration_kind,
                "state": state,
                "setup_revision": setup_revision,
                "settings": settings,
                "provider_agent_display_name": provider_agent_display_name,
                "provider_config": provider_config,
                "capabilities": capabilities,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if last_oauth_flow_id is not UNSET:
            field_dict["last_oauth_flow_id"] = last_oauth_flow_id
        if runtime_failure is not UNSET:
            field_dict["runtime_failure"] = runtime_failure
        if provider_tenant_id is not UNSET:
            field_dict["provider_tenant_id"] = provider_tenant_id
        if provider_account_ref is not UNSET:
            field_dict["provider_account_ref"] = provider_account_ref
        if bot_mention is not UNSET:
            field_dict["bot_mention"] = bot_mention
        if credential_secret_id is not UNSET:
            field_dict["credential_secret_id"] = credential_secret_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.integration_capabilities import IntegrationCapabilities
        from ..models.integration_provider_config import IntegrationProviderConfig
        from ..models.integration_runtime_failure import IntegrationRuntimeFailure
        from ..models.integration_settings import IntegrationSettings

        d = dict(src_dict)
        id = d.pop("id")

        project_id = d.pop("project_id")

        name = d.pop("name")

        integration_kind = check_integration_kind(d.pop("integration_kind"))

        state = check_integration_state(d.pop("state"))

        setup_revision = d.pop("setup_revision")

        settings = IntegrationSettings.from_dict(d.pop("settings"))

        provider_agent_display_name = d.pop("provider_agent_display_name")

        provider_config = IntegrationProviderConfig.from_dict(d.pop("provider_config"))

        capabilities = IntegrationCapabilities.from_dict(d.pop("capabilities"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        last_oauth_flow_id = d.pop("last_oauth_flow_id", UNSET)

        _runtime_failure = d.pop("runtime_failure", UNSET)
        runtime_failure: Union[Unset, IntegrationRuntimeFailure]
        if isinstance(_runtime_failure, Unset):
            runtime_failure = UNSET
        else:
            runtime_failure = IntegrationRuntimeFailure.from_dict(_runtime_failure)

        provider_tenant_id = d.pop("provider_tenant_id", UNSET)

        provider_account_ref = d.pop("provider_account_ref", UNSET)

        bot_mention = d.pop("bot_mention", UNSET)

        credential_secret_id = d.pop("credential_secret_id", UNSET)

        integration = cls(
            id=id,
            project_id=project_id,
            name=name,
            integration_kind=integration_kind,
            state=state,
            setup_revision=setup_revision,
            settings=settings,
            provider_agent_display_name=provider_agent_display_name,
            provider_config=provider_config,
            capabilities=capabilities,
            created_at=created_at,
            updated_at=updated_at,
            last_oauth_flow_id=last_oauth_flow_id,
            runtime_failure=runtime_failure,
            provider_tenant_id=provider_tenant_id,
            provider_account_ref=provider_account_ref,
            bot_mention=bot_mention,
            credential_secret_id=credential_secret_id,
        )

        return integration
