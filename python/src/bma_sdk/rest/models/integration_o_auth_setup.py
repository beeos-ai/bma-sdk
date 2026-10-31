import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="IntegrationOAuthSetup")


@_attrs_define
class IntegrationOAuthSetup:
    """
    Attributes:
        integration_id (str):
        setup_revision (int): Integration setup revision captured by this authorization flow.
        provider (str):
        flow_id (str):
        oauth_url (str):
        redirect_uri (str):
        events_url (str):
        actions_url (str):
        expires_at (datetime.datetime):
    """

    integration_id: str
    setup_revision: int
    provider: str
    flow_id: str
    oauth_url: str
    redirect_uri: str
    events_url: str
    actions_url: str
    expires_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        integration_id = self.integration_id

        setup_revision = self.setup_revision

        provider = self.provider

        flow_id = self.flow_id

        oauth_url = self.oauth_url

        redirect_uri = self.redirect_uri

        events_url = self.events_url

        actions_url = self.actions_url

        expires_at = self.expires_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "integration_id": integration_id,
                "setup_revision": setup_revision,
                "provider": provider,
                "flow_id": flow_id,
                "oauth_url": oauth_url,
                "redirect_uri": redirect_uri,
                "events_url": events_url,
                "actions_url": actions_url,
                "expires_at": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        integration_id = d.pop("integration_id")

        setup_revision = d.pop("setup_revision")

        provider = d.pop("provider")

        flow_id = d.pop("flow_id")

        oauth_url = d.pop("oauth_url")

        redirect_uri = d.pop("redirect_uri")

        events_url = d.pop("events_url")

        actions_url = d.pop("actions_url")

        expires_at = isoparse(d.pop("expires_at"))

        integration_o_auth_setup = cls(
            integration_id=integration_id,
            setup_revision=setup_revision,
            provider=provider,
            flow_id=flow_id,
            oauth_url=oauth_url,
            redirect_uri=redirect_uri,
            events_url=events_url,
            actions_url=actions_url,
            expires_at=expires_at,
        )

        return integration_o_auth_setup
