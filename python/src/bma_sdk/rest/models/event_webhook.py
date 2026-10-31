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

from ..models.event_webhook_event_type import (
    EventWebhookEventType,
    check_event_webhook_event_type,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_event_webhook_scope import AgentEventWebhookScope
    from ..models.agent_profile_event_webhook_scope import AgentProfileEventWebhookScope
    from ..models.project_event_webhook_scope import ProjectEventWebhookScope


T = TypeVar("T", bound="EventWebhook")


@_attrs_define
class EventWebhook:
    """
    Attributes:
        url (str): Public HTTPS endpoint, at most 2048 bytes after URL encoding.
        event_types (list[EventWebhookEventType]):
        scope (Union['AgentEventWebhookScope', 'AgentProfileEventWebhookScope', 'ProjectEventWebhookScope']):
        id (str):
        org_id (str):
        project_id (str): Project ID (proj_...).
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        signing_secret_id (Union[Unset, str]): Secret ID (sec_...).
    """

    url: str
    event_types: list[EventWebhookEventType]
    scope: Union[
        "AgentEventWebhookScope",
        "AgentProfileEventWebhookScope",
        "ProjectEventWebhookScope",
    ]
    id: str
    org_id: str
    project_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    signing_secret_id: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.agent_profile_event_webhook_scope import (
            AgentProfileEventWebhookScope,
        )
        from ..models.project_event_webhook_scope import ProjectEventWebhookScope

        url = self.url

        event_types = []
        for event_types_item_data in self.event_types:
            event_types_item: str = event_types_item_data
            event_types.append(event_types_item)

        scope: dict[str, Any]
        if isinstance(self.scope, ProjectEventWebhookScope):
            scope = self.scope.to_dict()
        elif isinstance(self.scope, AgentProfileEventWebhookScope):
            scope = self.scope.to_dict()
        else:
            scope = self.scope.to_dict()

        id = self.id

        org_id = self.org_id

        project_id = self.project_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        signing_secret_id = self.signing_secret_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "url": url,
                "event_types": event_types,
                "scope": scope,
                "id": id,
                "org_id": org_id,
                "project_id": project_id,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )
        if signing_secret_id is not UNSET:
            field_dict["signing_secret_id"] = signing_secret_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_event_webhook_scope import AgentEventWebhookScope
        from ..models.agent_profile_event_webhook_scope import (
            AgentProfileEventWebhookScope,
        )
        from ..models.project_event_webhook_scope import ProjectEventWebhookScope

        d = dict(src_dict)
        url = d.pop("url")

        event_types = []
        _event_types = d.pop("event_types")
        for event_types_item_data in _event_types:
            event_types_item = check_event_webhook_event_type(event_types_item_data)

            event_types.append(event_types_item)

        def _parse_scope(
            data: object,
        ) -> Union[
            "AgentEventWebhookScope",
            "AgentProfileEventWebhookScope",
            "ProjectEventWebhookScope",
        ]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_event_webhook_scope_type_0 = (
                    ProjectEventWebhookScope.from_dict(data)
                )

                return componentsschemas_event_webhook_scope_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_event_webhook_scope_type_1 = (
                    AgentProfileEventWebhookScope.from_dict(data)
                )

                return componentsschemas_event_webhook_scope_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_event_webhook_scope_type_2 = (
                AgentEventWebhookScope.from_dict(data)
            )

            return componentsschemas_event_webhook_scope_type_2

        scope = _parse_scope(d.pop("scope"))

        id = d.pop("id")

        org_id = d.pop("org_id")

        project_id = d.pop("project_id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        signing_secret_id = d.pop("signing_secret_id", UNSET)

        event_webhook = cls(
            url=url,
            event_types=event_types,
            scope=scope,
            id=id,
            org_id=org_id,
            project_id=project_id,
            created_at=created_at,
            updated_at=updated_at,
            signing_secret_id=signing_secret_id,
        )

        return event_webhook
