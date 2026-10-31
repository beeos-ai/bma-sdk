from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.model_provider_auth_kind import (
    ModelProviderAuthKind,
    check_model_provider_auth_kind,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_model_provider_config_request_auth_options import (
        UpdateModelProviderConfigRequestAuthOptions,
    )
    from ..models.update_model_provider_config_request_headers import (
        UpdateModelProviderConfigRequestHeaders,
    )
    from ..models.update_model_provider_config_request_secret_headers import (
        UpdateModelProviderConfigRequestSecretHeaders,
    )


T = TypeVar("T", bound="UpdateModelProviderConfigRequest")


@_attrs_define
class UpdateModelProviderConfigRequest:
    """Update a provider config. Omitted fields keep their current values.

    Attributes:
        base_url (Union[Unset, str]): Provider endpoint base URL. Normal API mode requires a public HTTPS endpoint;
            localhost and loopback endpoints are accepted only when the API is running in insecure dev mode.
        endpoint_path (Union[Unset, str]): URL path under base_url. This changes where requests are sent, not which API
            format BMA speaks.
        request_timeout_ms (Union[Unset, int]): Total deadline for one provider attempt, including reasoning and
            response streaming, in milliseconds. Retries have separate deadlines.
        idle_timeout_ms (Union[Unset, int]): Maximum wait for response headers or the next response bytes, in
            milliseconds. Heartbeats count as activity. Local response processing does not consume this idle budget.
        auth_kind (Union[Unset, ModelProviderAuthKind]): How the credential is sent: bearer_token, api_key_header, or
            sigv4 (AWS).
        auth_options (Union[Unset, UpdateModelProviderConfigRequestAuthOptions]): Non-secret authentication settings.
            Use an empty object with bearer_token. With api_key_header, set {"header_name":"..."}. With sigv4, set the AWS
            signing service and region.
        credential_secret_id (Union[Unset, str]): Secret ID (sec_...).
        headers (Union[Unset, UpdateModelProviderConfigRequestHeaders]): Extra HTTP headers sent with every request to
            this provider. Values are stored and returned as plain text; use secret_headers for keys and tokens. Replaces
            all headers when provided.
        secret_headers (Union[Unset, UpdateModelProviderConfigRequestSecretHeaders]): Extra HTTP headers whose values
            come from org-owned generic secrets, mapping header names to secret references. Replaces all secret headers when
            provided.
    """

    base_url: Union[Unset, str] = UNSET
    endpoint_path: Union[Unset, str] = UNSET
    request_timeout_ms: Union[Unset, int] = UNSET
    idle_timeout_ms: Union[Unset, int] = UNSET
    auth_kind: Union[Unset, ModelProviderAuthKind] = UNSET
    auth_options: Union[Unset, "UpdateModelProviderConfigRequestAuthOptions"] = UNSET
    credential_secret_id: Union[Unset, str] = UNSET
    headers: Union[Unset, "UpdateModelProviderConfigRequestHeaders"] = UNSET
    secret_headers: Union[Unset, "UpdateModelProviderConfigRequestSecretHeaders"] = (
        UNSET
    )

    def to_dict(self) -> dict[str, Any]:
        base_url = self.base_url

        endpoint_path = self.endpoint_path

        request_timeout_ms = self.request_timeout_ms

        idle_timeout_ms = self.idle_timeout_ms

        auth_kind: Union[Unset, str] = UNSET
        if not isinstance(self.auth_kind, Unset):
            auth_kind = self.auth_kind

        auth_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.auth_options, Unset):
            auth_options = self.auth_options.to_dict()

        credential_secret_id = self.credential_secret_id

        headers: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.headers, Unset):
            headers = self.headers.to_dict()

        secret_headers: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.secret_headers, Unset):
            secret_headers = self.secret_headers.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if base_url is not UNSET:
            field_dict["base_url"] = base_url
        if endpoint_path is not UNSET:
            field_dict["endpoint_path"] = endpoint_path
        if request_timeout_ms is not UNSET:
            field_dict["request_timeout_ms"] = request_timeout_ms
        if idle_timeout_ms is not UNSET:
            field_dict["idle_timeout_ms"] = idle_timeout_ms
        if auth_kind is not UNSET:
            field_dict["auth_kind"] = auth_kind
        if auth_options is not UNSET:
            field_dict["auth_options"] = auth_options
        if credential_secret_id is not UNSET:
            field_dict["credential_secret_id"] = credential_secret_id
        if headers is not UNSET:
            field_dict["headers"] = headers
        if secret_headers is not UNSET:
            field_dict["secret_headers"] = secret_headers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_model_provider_config_request_auth_options import (
            UpdateModelProviderConfigRequestAuthOptions,
        )
        from ..models.update_model_provider_config_request_headers import (
            UpdateModelProviderConfigRequestHeaders,
        )
        from ..models.update_model_provider_config_request_secret_headers import (
            UpdateModelProviderConfigRequestSecretHeaders,
        )

        d = dict(src_dict)
        base_url = d.pop("base_url", UNSET)

        endpoint_path = d.pop("endpoint_path", UNSET)

        request_timeout_ms = d.pop("request_timeout_ms", UNSET)

        idle_timeout_ms = d.pop("idle_timeout_ms", UNSET)

        _auth_kind = d.pop("auth_kind", UNSET)
        auth_kind: Union[Unset, ModelProviderAuthKind]
        if isinstance(_auth_kind, Unset):
            auth_kind = UNSET
        else:
            auth_kind = check_model_provider_auth_kind(_auth_kind)

        _auth_options = d.pop("auth_options", UNSET)
        auth_options: Union[Unset, UpdateModelProviderConfigRequestAuthOptions]
        if isinstance(_auth_options, Unset):
            auth_options = UNSET
        else:
            auth_options = UpdateModelProviderConfigRequestAuthOptions.from_dict(
                _auth_options
            )

        credential_secret_id = d.pop("credential_secret_id", UNSET)

        _headers = d.pop("headers", UNSET)
        headers: Union[Unset, UpdateModelProviderConfigRequestHeaders]
        if isinstance(_headers, Unset):
            headers = UNSET
        else:
            headers = UpdateModelProviderConfigRequestHeaders.from_dict(_headers)

        _secret_headers = d.pop("secret_headers", UNSET)
        secret_headers: Union[Unset, UpdateModelProviderConfigRequestSecretHeaders]
        if isinstance(_secret_headers, Unset):
            secret_headers = UNSET
        else:
            secret_headers = UpdateModelProviderConfigRequestSecretHeaders.from_dict(
                _secret_headers
            )

        update_model_provider_config_request = cls(
            base_url=base_url,
            endpoint_path=endpoint_path,
            request_timeout_ms=request_timeout_ms,
            idle_timeout_ms=idle_timeout_ms,
            auth_kind=auth_kind,
            auth_options=auth_options,
            credential_secret_id=credential_secret_id,
            headers=headers,
            secret_headers=secret_headers,
        )

        return update_model_provider_config_request
