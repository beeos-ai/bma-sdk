from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

from ..models.direct_secret_availability_source import (
    DirectSecretAvailabilitySource,
    check_direct_secret_availability_source,
)

T = TypeVar("T", bound="DirectSecretAvailability")


@_attrs_define
class DirectSecretAvailability:
    """
    Attributes:
        source (DirectSecretAvailabilitySource):
        project_id (str): Project ID (proj_...).
    """

    source: DirectSecretAvailabilitySource
    project_id: str

    def to_dict(self) -> dict[str, Any]:
        source: str = self.source

        project_id = self.project_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "source": source,
                "project_id": project_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = check_direct_secret_availability_source(d.pop("source"))

        project_id = d.pop("project_id")

        direct_secret_availability = cls(
            source=source,
            project_id=project_id,
        )

        return direct_secret_availability
