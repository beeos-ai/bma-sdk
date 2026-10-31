from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.personal_access_token import PersonalAccessToken


T = TypeVar("T", bound="CreatePersonalAccessTokenResponse")


@_attrs_define
class CreatePersonalAccessTokenResponse:
    """
    Attributes:
        token (str): Opaque bearer credential.
        token_record (PersonalAccessToken):
    """

    token: str
    token_record: "PersonalAccessToken"

    def to_dict(self) -> dict[str, Any]:
        token = self.token

        token_record = self.token_record.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "token": token,
                "token_record": token_record,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.personal_access_token import PersonalAccessToken

        d = dict(src_dict)
        token = d.pop("token")

        token_record = PersonalAccessToken.from_dict(d.pop("token_record"))

        create_personal_access_token_response = cls(
            token=token,
            token_record=token_record,
        )

        return create_personal_access_token_response
