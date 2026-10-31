from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.create_model_provider_config_request_preset import (
    CreateModelProviderConfigRequestPreset,
    check_create_model_provider_config_request_preset,
)
from ..models.model_api_format import ModelAPIFormat, check_model_api_format
from ..models.model_provider_api_variant import (
    ModelProviderAPIVariant,
    check_model_provider_api_variant,
)
from ..models.model_provider_auth_kind import (
    ModelProviderAuthKind,
    check_model_provider_auth_kind,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_model_provider_config_request_auth_options import (
        CreateModelProviderConfigRequestAuthOptions,
    )
    from ..models.create_model_provider_config_request_headers import (
        CreateModelProviderConfigRequestHeaders,
    )
    from ..models.create_model_provider_config_request_secret_headers import (
        CreateModelProviderConfigRequestSecretHeaders,
    )


T = TypeVar("T", bound="CreateModelProviderConfigRequest")


@_attrs_define
class CreateModelProviderConfigRequest:
    """Connect BMA to a model API endpoint. Use a preset for built-in providers, or provide api_format and base_url for a
    custom endpoint. When omitted, endpoint_path and auth settings are filled from api_format.

        Attributes:
            name (str): Human-readable name. Spaces and punctuation are allowed; leading or trailing whitespace and
                invisible or control characters are not.
            credential_secret_id (str): Secret ID (sec_...).
            preset (Union[Unset, CreateModelProviderConfigRequestPreset]): Built-in provider settings: openai, openrouter,
                or anthropic. A preset fills in api_format, api_variant, base_url, endpoint_path, auth_kind, and auth_options,
                so omit those when using one.
            api_format (Union[Unset, ModelAPIFormat]): Wire protocol the model endpoint speaks: openai-responses, openai-
                chat-completions, or anthropic-messages.
            api_variant (Union[Unset, ModelProviderAPIVariant]): Provider-specific flavor of the API format: default,
                openrouter, or bedrock.
            base_url (Union[Unset, str]): Provider endpoint base URL. Normal API mode requires a public HTTPS endpoint;
                localhost and loopback endpoints are accepted only when the API is running in insecure dev mode.
            endpoint_path (Union[Unset, str]): URL path under base_url. Defaults to /responses for OpenAI Responses,
                /chat/completions for Chat Completions, and /messages for Anthropic Messages.
            request_timeout_ms (Union[Unset, int]): Total deadline for one provider attempt, including reasoning and
                response streaming, in milliseconds. Defaults to 3600000 (60 minutes). Retries have separate deadlines.
            idle_timeout_ms (Union[Unset, int]): Maximum wait for response headers or the next response bytes, in
                milliseconds. Heartbeats count as activity. Defaults to 300000 (5 minutes). Local response processing does not
                consume this idle budget.
            auth_kind (Union[Unset, ModelProviderAuthKind]): How the credential is sent: bearer_token, api_key_header, or
                sigv4 (AWS).
            auth_options (Union[Unset, CreateModelProviderConfigRequestAuthOptions]): Non-secret authentication settings.
                Use an empty object with bearer_token. With api_key_header, set {"header_name":"..."}; Anthropic Messages
                defaults to {"header_name":"x-api-key"}. With sigv4, set the AWS signing service and region.
            headers (Union[Unset, CreateModelProviderConfigRequestHeaders]): Extra HTTP headers sent with every request to
                this provider. Values are stored and returned as plain text; use secret_headers for keys and tokens.
            secret_headers (Union[Unset, CreateModelProviderConfigRequestSecretHeaders]): Extra HTTP headers whose values
                come from org-owned generic secrets, mapping header names to secret references.
    """

    name: str
    credential_secret_id: str
    preset: Union[Unset, CreateModelProviderConfigRequestPreset] = UNSET
    api_format: Union[Unset, ModelAPIFormat] = UNSET
    api_variant: Union[Unset, ModelProviderAPIVariant] = UNSET
    base_url: Union[Unset, str] = UNSET
    endpoint_path: Union[Unset, str] = UNSET
    request_timeout_ms: Union[Unset, int] = UNSET
    idle_timeout_ms: Union[Unset, int] = UNSET
    auth_kind: Union[Unset, ModelProviderAuthKind] = UNSET
    auth_options: Union[Unset, "CreateModelProviderConfigRequestAuthOptions"] = UNSET
    headers: Union[Unset, "CreateModelProviderConfigRequestHeaders"] = UNSET
    secret_headers: Union[Unset, "CreateModelProviderConfigRequestSecretHeaders"] = (
        UNSET
    )

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        credential_secret_id = self.credential_secret_id

        preset: Union[Unset, str] = UNSET
        if not isinstance(self.preset, Unset):
            preset = self.preset

        api_format: Union[Unset, str] = UNSET
        if not isinstance(self.api_format, Unset):
            api_format = self.api_format

        api_variant: Union[Unset, str] = UNSET
        if not isinstance(self.api_variant, Unset):
            api_variant = self.api_variant

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

        headers: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.headers, Unset):
            headers = self.headers.to_dict()

        secret_headers: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.secret_headers, Unset):
            secret_headers = self.secret_headers.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "credential_secret_id": credential_secret_id,
            }
        )
        if preset is not UNSET:
            field_dict["preset"] = preset
        if api_format is not UNSET:
            field_dict["api_format"] = api_format
        if api_variant is not UNSET:
            field_dict["api_variant"] = api_variant
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
        if headers is not UNSET:
            field_dict["headers"] = headers
        if secret_headers is not UNSET:
            field_dict["secret_headers"] = secret_headers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_model_provider_config_request_auth_options import (
            CreateModelProviderConfigRequestAuthOptions,
        )
        from ..models.create_model_provider_config_request_headers import (
            CreateModelProviderConfigRequestHeaders,
        )
        from ..models.create_model_provider_config_request_secret_headers import (
            CreateModelProviderConfigRequestSecretHeaders,
        )

        d = dict(src_dict)
        name = d.pop("name")

        credential_secret_id = d.pop("credential_secret_id")

        _preset = d.pop("preset", UNSET)
        preset: Union[Unset, CreateModelProviderConfigRequestPreset]
        if isinstance(_preset, Unset):
            preset = UNSET
        else:
            preset = check_create_model_provider_config_request_preset(_preset)

        _api_format = d.pop("api_format", UNSET)
        api_format: Union[Unset, ModelAPIFormat]
        if isinstance(_api_format, Unset):
            api_format = UNSET
        else:
            api_format = check_model_api_format(_api_format)

        _api_variant = d.pop("api_variant", UNSET)
        api_variant: Union[Unset, ModelProviderAPIVariant]
        if isinstance(_api_variant, Unset):
            api_variant = UNSET
        else:
            api_variant = check_model_provider_api_variant(_api_variant)

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
        auth_options: Union[Unset, CreateModelProviderConfigRequestAuthOptions]
        if isinstance(_auth_options, Unset):
            auth_options = UNSET
        else:
            auth_options = CreateModelProviderConfigRequestAuthOptions.from_dict(
                _auth_options
            )

        _headers = d.pop("headers", UNSET)
        headers: Union[Unset, CreateModelProviderConfigRequestHeaders]
        if isinstance(_headers, Unset):
            headers = UNSET
        else:
            headers = CreateModelProviderConfigRequestHeaders.from_dict(_headers)

        _secret_headers = d.pop("secret_headers", UNSET)
        secret_headers: Union[Unset, CreateModelProviderConfigRequestSecretHeaders]
        if isinstance(_secret_headers, Unset):
            secret_headers = UNSET
        else:
            secret_headers = CreateModelProviderConfigRequestSecretHeaders.from_dict(
                _secret_headers
            )

        create_model_provider_config_request = cls(
            name=name,
            credential_secret_id=credential_secret_id,
            preset=preset,
            api_format=api_format,
            api_variant=api_variant,
            base_url=base_url,
            endpoint_path=endpoint_path,
            request_timeout_ms=request_timeout_ms,
            idle_timeout_ms=idle_timeout_ms,
            auth_kind=auth_kind,
            auth_options=auth_options,
            headers=headers,
            secret_headers=secret_headers,
        )

        return create_model_provider_config_request
