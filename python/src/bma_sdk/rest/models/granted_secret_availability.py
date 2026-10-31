from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.granted_secret_availability_source import (
    GrantedSecretAvailabilitySource,
    check_granted_secret_availability_source,
)

T = TypeVar("T", bound="GrantedSecretAvailability")


@_attrs_define
class GrantedSecretAvailability:
    """
    Attributes:
        source (GrantedSecretAvailabilitySource):
        project_id (str): Project ID (proj_...).
        grant_id (str):
    """

    source: GrantedSecretAvailabilitySource
    project_id: str
    grant_id: str

    def to_dict(self) -> dict[str, Any]:
        source: str = self.source

        project_id = self.project_id

        grant_id = self.grant_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "source": source,
                "project_id": project_id,
                "grant_id": grant_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = check_granted_secret_availability_source(d.pop("source"))

        project_id = d.pop("project_id")

        grant_id = d.pop("grant_id")

        granted_secret_availability = cls(
            source=source,
            project_id=project_id,
            grant_id=grant_id,
        )

        return granted_secret_availability
