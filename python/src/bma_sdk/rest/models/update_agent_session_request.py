import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_agent_session_request_metadata import (
        UpdateAgentSessionRequestMetadata,
    )


T = TypeVar("T", bound="UpdateAgentSessionRequest")


@_attrs_define
class UpdateAgentSessionRequest:
    """
    Attributes:
        agent_config_id (Union[Unset, str]):
        environment_id (Union[None, UUID, Unset]):
        metadata (Union[Unset, UpdateAgentSessionRequestMetadata]):
        expected_updated_at (Union[Unset, datetime.datetime]): Optimistic version check. The update applies only while
            the session's updated_at still equals this value; otherwise it answers 409 conflict. Anything that writes the
            session (an update, the automatic title) moves updated_at.
    """

    agent_config_id: Union[Unset, str] = UNSET
    environment_id: Union[None, UUID, Unset] = UNSET
    metadata: Union[Unset, "UpdateAgentSessionRequestMetadata"] = UNSET
    expected_updated_at: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> dict[str, Any]:
        agent_config_id = self.agent_config_id

        environment_id: Union[None, Unset, str]
        if isinstance(self.environment_id, Unset):
            environment_id = UNSET
        elif isinstance(self.environment_id, UUID):
            environment_id = str(self.environment_id)
        else:
            environment_id = self.environment_id

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        expected_updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.expected_updated_at, Unset):
            expected_updated_at = self.expected_updated_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if agent_config_id is not UNSET:
            field_dict["agent_config_id"] = agent_config_id
        if environment_id is not UNSET:
            field_dict["environment_id"] = environment_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if expected_updated_at is not UNSET:
            field_dict["expected_updated_at"] = expected_updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_agent_session_request_metadata import (
            UpdateAgentSessionRequestMetadata,
        )

        d = dict(src_dict)
        agent_config_id = d.pop("agent_config_id", UNSET)

        def _parse_environment_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                environment_id_type_0 = UUID(data)

                return environment_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        environment_id = _parse_environment_id(d.pop("environment_id", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, UpdateAgentSessionRequestMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = UpdateAgentSessionRequestMetadata.from_dict(_metadata)

        _expected_updated_at = d.pop("expected_updated_at", UNSET)
        expected_updated_at: Union[Unset, datetime.datetime]
        if isinstance(_expected_updated_at, Unset):
            expected_updated_at = UNSET
        else:
            expected_updated_at = isoparse(_expected_updated_at)

        update_agent_session_request = cls(
            agent_config_id=agent_config_id,
            environment_id=environment_id,
            metadata=metadata,
            expected_updated_at=expected_updated_at,
        )

        return update_agent_session_request
