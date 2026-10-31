from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateIntegrationOAuthSetupRequest")


@_attrs_define
class CreateIntegrationOAuthSetupRequest:
    """
    Attributes:
        client_id (str):
        client_secret (str):
        signing_secret (str):
        return_to (Union[Unset, str]):
    """

    client_id: str
    client_secret: str
    signing_secret: str
    return_to: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        client_id = self.client_id

        client_secret = self.client_secret

        signing_secret = self.signing_secret

        return_to = self.return_to

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "signing_secret": signing_secret,
            }
        )
        if return_to is not UNSET:
            field_dict["return_to"] = return_to

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        client_id = d.pop("client_id")

        client_secret = d.pop("client_secret")

        signing_secret = d.pop("signing_secret")

        return_to = d.pop("return_to", UNSET)

        create_integration_o_auth_setup_request = cls(
            client_id=client_id,
            client_secret=client_secret,
            signing_secret=signing_secret,
            return_to=return_to,
        )

        return create_integration_o_auth_setup_request
