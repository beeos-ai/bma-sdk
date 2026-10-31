import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.agent_model_override_status import (
    AgentModelOverrideStatus,
    check_agent_model_override_status,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="AgentModelOverride")


@_attrs_define
class AgentModelOverride:
    """
    Attributes:
        id (str):
        agent_id (str):
        session_id (str):
        model (str):
        api_format (str):
        base_url (str):
        fingerprint (str): First 16 hex chars of sha256(key).
        status (AgentModelOverrideStatus):
        created_at (datetime.datetime):
        expires_with_session (bool): The override stays active until its session is archived.
        api_variant (Union[Unset, str]):
        endpoint_path (Union[Unset, str]):
        key_hint (Union[Unset, str]): Last 4 characters of the key, never the key.
        consume_after_turn (Union[Unset, bool]):
        expires_at (Union[None, Unset, datetime.datetime]): Absent for a session-lifetime override.
        revoked_at (Union[Unset, datetime.datetime]):
    """

    id: str
    agent_id: str
    session_id: str
    model: str
    api_format: str
    base_url: str
    fingerprint: str
    status: AgentModelOverrideStatus
    created_at: datetime.datetime
    expires_with_session: bool
    api_variant: Union[Unset, str] = UNSET
    endpoint_path: Union[Unset, str] = UNSET
    key_hint: Union[Unset, str] = UNSET
    consume_after_turn: Union[Unset, bool] = UNSET
    expires_at: Union[None, Unset, datetime.datetime] = UNSET
    revoked_at: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        agent_id = self.agent_id

        session_id = self.session_id

        model = self.model

        api_format = self.api_format

        base_url = self.base_url

        fingerprint = self.fingerprint

        status: str = self.status

        created_at = self.created_at.isoformat()

        expires_with_session = self.expires_with_session

        api_variant = self.api_variant

        endpoint_path = self.endpoint_path

        key_hint = self.key_hint

        consume_after_turn = self.consume_after_turn

        expires_at: Union[None, Unset, str]
        if isinstance(self.expires_at, Unset):
            expires_at = UNSET
        elif isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        revoked_at: Union[Unset, str] = UNSET
        if not isinstance(self.revoked_at, Unset):
            revoked_at = self.revoked_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "agent_id": agent_id,
                "session_id": session_id,
                "model": model,
                "api_format": api_format,
                "base_url": base_url,
                "fingerprint": fingerprint,
                "status": status,
                "created_at": created_at,
                "expires_with_session": expires_with_session,
            }
        )
        if api_variant is not UNSET:
            field_dict["api_variant"] = api_variant
        if endpoint_path is not UNSET:
            field_dict["endpoint_path"] = endpoint_path
        if key_hint is not UNSET:
            field_dict["key_hint"] = key_hint
        if consume_after_turn is not UNSET:
            field_dict["consume_after_turn"] = consume_after_turn
        if expires_at is not UNSET:
            field_dict["expires_at"] = expires_at
        if revoked_at is not UNSET:
            field_dict["revoked_at"] = revoked_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        agent_id = d.pop("agent_id")

        session_id = d.pop("session_id")

        model = d.pop("model")

        api_format = d.pop("api_format")

        base_url = d.pop("base_url")

        fingerprint = d.pop("fingerprint")

        status = check_agent_model_override_status(d.pop("status"))

        created_at = isoparse(d.pop("created_at"))

        expires_with_session = d.pop("expires_with_session")

        api_variant = d.pop("api_variant", UNSET)

        endpoint_path = d.pop("endpoint_path", UNSET)

        key_hint = d.pop("key_hint", UNSET)

        consume_after_turn = d.pop("consume_after_turn", UNSET)

        def _parse_expires_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = isoparse(data)

                return expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        expires_at = _parse_expires_at(d.pop("expires_at", UNSET))

        _revoked_at = d.pop("revoked_at", UNSET)
        revoked_at: Union[Unset, datetime.datetime]
        if isinstance(_revoked_at, Unset):
            revoked_at = UNSET
        else:
            revoked_at = isoparse(_revoked_at)

        agent_model_override = cls(
            id=id,
            agent_id=agent_id,
            session_id=session_id,
            model=model,
            api_format=api_format,
            base_url=base_url,
            fingerprint=fingerprint,
            status=status,
            created_at=created_at,
            expires_with_session=expires_with_session,
            api_variant=api_variant,
            endpoint_path=endpoint_path,
            key_hint=key_hint,
            consume_after_turn=consume_after_turn,
            expires_at=expires_at,
            revoked_at=revoked_at,
        )

        return agent_model_override
