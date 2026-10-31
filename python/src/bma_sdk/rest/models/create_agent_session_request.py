from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)
from uuid import UUID

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_model_override_input import AgentModelOverrideInput
    from ..models.create_agent_config_request import CreateAgentConfigRequest
    from ..models.create_agent_session_request_metadata import (
        CreateAgentSessionRequestMetadata,
    )


T = TypeVar("T", bound="CreateAgentSessionRequest")


@_attrs_define
class CreateAgentSessionRequest:
    """
    Attributes:
        agent_config_id (Union[Unset, str]):
        config_source (Union[Unset, CreateAgentConfigRequest]): An agent config to compile. YAML sources are stored
            verbatim, so comments and formatting survive; JSON sources, as text or as an object, are stored canonicalized,
            so the same JSON definition always maps to the same config.
        environment_id (Union[Unset, UUID]):
        idempotency_key (Union[Unset, str]): Replays the original session for this agent. A replay with a different
            pinned config, environment or metadata is a 409 conflict.
        model_override (Union[Unset, AgentModelOverrideInput]):
        metadata (Union[Unset, CreateAgentSessionRequestMetadata]):
    """

    agent_config_id: Union[Unset, str] = UNSET
    config_source: Union[Unset, "CreateAgentConfigRequest"] = UNSET
    environment_id: Union[Unset, UUID] = UNSET
    idempotency_key: Union[Unset, str] = UNSET
    model_override: Union[Unset, "AgentModelOverrideInput"] = UNSET
    metadata: Union[Unset, "CreateAgentSessionRequestMetadata"] = UNSET

    def to_dict(self) -> dict[str, Any]:
        agent_config_id = self.agent_config_id

        config_source: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.config_source, Unset):
            config_source = self.config_source.to_dict()

        environment_id: Union[Unset, str] = UNSET
        if not isinstance(self.environment_id, Unset):
            environment_id = str(self.environment_id)

        idempotency_key = self.idempotency_key

        model_override: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.model_override, Unset):
            model_override = self.model_override.to_dict()

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if agent_config_id is not UNSET:
            field_dict["agent_config_id"] = agent_config_id
        if config_source is not UNSET:
            field_dict["config_source"] = config_source
        if environment_id is not UNSET:
            field_dict["environment_id"] = environment_id
        if idempotency_key is not UNSET:
            field_dict["idempotency_key"] = idempotency_key
        if model_override is not UNSET:
            field_dict["model_override"] = model_override
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_model_override_input import AgentModelOverrideInput
        from ..models.create_agent_config_request import CreateAgentConfigRequest
        from ..models.create_agent_session_request_metadata import (
            CreateAgentSessionRequestMetadata,
        )

        d = dict(src_dict)
        agent_config_id = d.pop("agent_config_id", UNSET)

        _config_source = d.pop("config_source", UNSET)
        config_source: Union[Unset, CreateAgentConfigRequest]
        if isinstance(_config_source, Unset):
            config_source = UNSET
        else:
            config_source = CreateAgentConfigRequest.from_dict(_config_source)

        _environment_id = d.pop("environment_id", UNSET)
        environment_id: Union[Unset, UUID]
        if isinstance(_environment_id, Unset):
            environment_id = UNSET
        else:
            environment_id = UUID(_environment_id)

        idempotency_key = d.pop("idempotency_key", UNSET)

        _model_override = d.pop("model_override", UNSET)
        model_override: Union[Unset, AgentModelOverrideInput]
        if isinstance(_model_override, Unset):
            model_override = UNSET
        else:
            model_override = AgentModelOverrideInput.from_dict(_model_override)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, CreateAgentSessionRequestMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CreateAgentSessionRequestMetadata.from_dict(_metadata)

        create_agent_session_request = cls(
            agent_config_id=agent_config_id,
            config_source=config_source,
            environment_id=environment_id,
            idempotency_key=idempotency_key,
            model_override=model_override,
            metadata=metadata,
        )

        return create_agent_session_request
