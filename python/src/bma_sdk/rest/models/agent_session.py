import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.agent_session_config_origin import (
    AgentSessionConfigOrigin,
    check_agent_session_config_origin,
)
from ..models.agent_session_state import AgentSessionState, check_agent_session_state
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_session_metadata import AgentSessionMetadata


T = TypeVar("T", bound="AgentSession")


@_attrs_define
class AgentSession:
    """
    Attributes:
        id (str):
        org_id (str):
        project_id (str):
        agent_id (str):
        agent_config_id (str):
        config_origin (AgentSessionConfigOrigin): `agent` follows agents.current_config_id (the default session only);
            `session` pins this session to its immutable agent_config_id.
        state (AgentSessionState):
        is_default (bool):
        next_turn_sequence (int):
        next_event_sequence (int):
        metadata (AgentSessionMetadata):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        environment_id (Union[None, Unset, str]): Opaque UHP environment reference.
        archived_at (Union[None, Unset, datetime.datetime]):
    """

    id: str
    org_id: str
    project_id: str
    agent_id: str
    agent_config_id: str
    config_origin: AgentSessionConfigOrigin
    state: AgentSessionState
    is_default: bool
    next_turn_sequence: int
    next_event_sequence: int
    metadata: "AgentSessionMetadata"
    created_at: datetime.datetime
    updated_at: datetime.datetime
    environment_id: Union[None, Unset, str] = UNSET
    archived_at: Union[None, Unset, datetime.datetime] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        agent_id = self.agent_id

        agent_config_id = self.agent_config_id

        config_origin: str = self.config_origin

        state: str = self.state

        is_default = self.is_default

        next_turn_sequence = self.next_turn_sequence

        next_event_sequence = self.next_event_sequence

        metadata = self.metadata.to_dict()

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        environment_id: Union[None, Unset, str]
        if isinstance(self.environment_id, Unset):
            environment_id = UNSET
        else:
            environment_id = self.environment_id

        archived_at: Union[None, Unset, str]
        if isinstance(self.archived_at, Unset):
            archived_at = UNSET
        elif isinstance(self.archived_at, datetime.datetime):
            archived_at = self.archived_at.isoformat()
        else:
            archived_at = self.archived_at

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "agent_id": agent_id,
                "agent_config_id": agent_config_id,
                "config_origin": config_origin,
                "state": state,
                "is_default": is_default,
                "next_turn_sequence": next_turn_sequence,
                "next_event_sequence": next_event_sequence,
                "metadata": metadata,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if environment_id is not UNSET:
            field_dict["environment_id"] = environment_id
        if archived_at is not UNSET:
            field_dict["archived_at"] = archived_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_session_metadata import AgentSessionMetadata

        d = dict(src_dict)
        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        agent_id = d.pop("agent_id")

        agent_config_id = d.pop("agent_config_id")

        config_origin = check_agent_session_config_origin(d.pop("config_origin"))

        state = check_agent_session_state(d.pop("state"))

        is_default = d.pop("is_default")

        next_turn_sequence = d.pop("next_turn_sequence")

        next_event_sequence = d.pop("next_event_sequence")

        metadata = AgentSessionMetadata.from_dict(d.pop("metadata"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_environment_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        environment_id = _parse_environment_id(d.pop("environment_id", UNSET))

        def _parse_archived_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                archived_at_type_0 = isoparse(data)

                return archived_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        archived_at = _parse_archived_at(d.pop("archived_at", UNSET))

        agent_session = cls(
            id=id,
            org_id=org_id,
            project_id=project_id,
            agent_id=agent_id,
            agent_config_id=agent_config_id,
            config_origin=config_origin,
            state=state,
            is_default=is_default,
            next_turn_sequence=next_turn_sequence,
            next_event_sequence=next_event_sequence,
            metadata=metadata,
            created_at=created_at,
            updated_at=updated_at,
            environment_id=environment_id,
            archived_at=archived_at,
        )

        return agent_session
