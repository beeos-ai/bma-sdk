from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.agent_session import AgentSession


T = TypeVar("T", bound="AgentSessionEnvelope")


@_attrs_define
class AgentSessionEnvelope:
    """
    Attributes:
        session (AgentSession):
    """

    session: "AgentSession"

    def to_dict(self) -> dict[str, Any]:
        session = self.session.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "session": session,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_session import AgentSession

        d = dict(src_dict)
        session = AgentSession.from_dict(d.pop("session"))

        agent_session_envelope = cls(
            session=session,
        )

        return agent_session_envelope
