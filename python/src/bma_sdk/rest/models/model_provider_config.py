import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.management_kind import ManagementKind, check_management_kind
from ..models.model_api_format import ModelAPIFormat, check_model_api_format

if TYPE_CHECKING:
    from ..models.model_provider_config_auth_options import (
        ModelProviderConfigAuthOptions,
    )
    from ..models.model_provider_config_headers import ModelProviderConfigHeaders
    from ..models.model_provider_config_secret_headers import (
        ModelProviderConfigSecretHeaders,
    )


T = TypeVar("T", bound="ModelProviderConfig")


@_attrs_define
class ModelProviderConfig:
    """
    Attributes:
        id (str):
        org_id (str):
        management_kind (ManagementKind): Lifecycle owner. Tenant-managed resources can be changed through tenant APIs.
            Cluster-managed resources are installed and lifecycle-managed by the control plane; individual APIs may
            explicitly expose tenant-editable settings.
        name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
            invisible or control characters are not.
        api_format (ModelAPIFormat): Wire protocol the model endpoint speaks: openai-responses, openai-chat-completions,
            or anthropic-messages.
        api_variant (str):
        base_url (str): Provider endpoint base URL. Normal API mode uses public HTTPS endpoints; localhost and loopback
            endpoints are only for insecure dev-mode configs.
        endpoint_path (str):
        request_timeout_ms (int):
        idle_timeout_ms (int):
        auth_kind (str):
        auth_options (ModelProviderConfigAuthOptions): Non-secret authentication settings for this provider config.
        credential_secret_id (str): Secret ID (sec_...).
        headers (ModelProviderConfigHeaders): Extra HTTP headers sent with every request to this provider.
        secret_headers (ModelProviderConfigSecretHeaders): Extra HTTP headers whose values come from the referenced
            secrets.
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: str
    org_id: str
    management_kind: ManagementKind
    name: str
    api_format: ModelAPIFormat
    api_variant: str
    base_url: str
    endpoint_path: str
    request_timeout_ms: int
    idle_timeout_ms: int
    auth_kind: str
    auth_options: "ModelProviderConfigAuthOptions"
    credential_secret_id: str
    headers: "ModelProviderConfigHeaders"
    secret_headers: "ModelProviderConfigSecretHeaders"
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        management_kind: str = self.management_kind

        name = self.name

        api_format: str = self.api_format

        api_variant = self.api_variant

        base_url = self.base_url

        endpoint_path = self.endpoint_path

        request_timeout_ms = self.request_timeout_ms

        idle_timeout_ms = self.idle_timeout_ms

        auth_kind = self.auth_kind

        auth_options = self.auth_options.to_dict()

        credential_secret_id = self.credential_secret_id

        headers = self.headers.to_dict()

        secret_headers = self.secret_headers.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "management_kind": management_kind,
                "name": name,
                "api_format": api_format,
                "api_variant": api_variant,
                "base_url": base_url,
                "endpoint_path": endpoint_path,
                "request_timeout_ms": request_timeout_ms,
                "idle_timeout_ms": idle_timeout_ms,
                "auth_kind": auth_kind,
                "auth_options": auth_options,
                "credential_secret_id": credential_secret_id,
                "headers": headers,
                "secret_headers": secret_headers,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.model_provider_config_auth_options import (
            ModelProviderConfigAuthOptions,
        )
        from ..models.model_provider_config_headers import ModelProviderConfigHeaders
        from ..models.model_provider_config_secret_headers import (
            ModelProviderConfigSecretHeaders,
        )

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        management_kind = check_management_kind(d.pop("management_kind"))

        name = d.pop("name")

        api_format = check_model_api_format(d.pop("api_format"))

        api_variant = d.pop("api_variant")

        base_url = d.pop("base_url")

        endpoint_path = d.pop("endpoint_path")

        request_timeout_ms = d.pop("request_timeout_ms")

        idle_timeout_ms = d.pop("idle_timeout_ms")

        auth_kind = d.pop("auth_kind")

        auth_options = ModelProviderConfigAuthOptions.from_dict(d.pop("auth_options"))

        credential_secret_id = d.pop("credential_secret_id")

        headers = ModelProviderConfigHeaders.from_dict(d.pop("headers"))

        secret_headers = ModelProviderConfigSecretHeaders.from_dict(
            d.pop("secret_headers")
        )

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        model_provider_config = cls(
            id=id,
            org_id=org_id,
            management_kind=management_kind,
            name=name,
            api_format=api_format,
            api_variant=api_variant,
            base_url=base_url,
            endpoint_path=endpoint_path,
            request_timeout_ms=request_timeout_ms,
            idle_timeout_ms=idle_timeout_ms,
            auth_kind=auth_kind,
            auth_options=auth_options,
            credential_secret_id=credential_secret_id,
            headers=headers,
            secret_headers=secret_headers,
            created_at=created_at,
            updated_at=updated_at,
        )

        return model_provider_config
