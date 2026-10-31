from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="InspectGitHubInstallationsRequest")


@_attrs_define
class InspectGitHubInstallationsRequest:
    """
    Attributes:
        credential_secret_id (str): Secret ID (sec_...).
        page (Union[Unset, int]):  Default: 1.
    """

    credential_secret_id: str
    page: Union[Unset, int] = 1

    def to_dict(self) -> dict[str, Any]:
        credential_secret_id = self.credential_secret_id

        page = self.page

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "credential_secret_id": credential_secret_id,
            }
        )
        if page is not UNSET:
            field_dict["page"] = page

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        credential_secret_id = d.pop("credential_secret_id")

        page = d.pop("page", UNSET)

        inspect_git_hub_installations_request = cls(
            credential_secret_id=credential_secret_id,
            page=page,
        )

        return inspect_git_hub_installations_request
