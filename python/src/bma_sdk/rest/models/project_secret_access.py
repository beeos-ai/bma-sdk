from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.direct_secret_availability import DirectSecretAvailability
    from ..models.granted_secret_availability import GrantedSecretAvailability
    from ..models.secret import Secret


T = TypeVar("T", bound="ProjectSecretAccess")


@_attrs_define
class ProjectSecretAccess:
    """
    Attributes:
        secret (Secret):
        availability (Union['DirectSecretAvailability', 'GrantedSecretAvailability']):
    """

    secret: "Secret"
    availability: Union["DirectSecretAvailability", "GrantedSecretAvailability"]

    def to_dict(self) -> dict[str, Any]:
        from ..models.direct_secret_availability import DirectSecretAvailability

        secret = self.secret.to_dict()

        availability: dict[str, Any]
        if isinstance(self.availability, DirectSecretAvailability):
            availability = self.availability.to_dict()
        else:
            availability = self.availability.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "secret": secret,
                "availability": availability,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.direct_secret_availability import DirectSecretAvailability
        from ..models.granted_secret_availability import GrantedSecretAvailability
        from ..models.secret import Secret

        d = dict(src_dict)
        secret = Secret.from_dict(d.pop("secret"))

        def _parse_availability(
            data: object,
        ) -> Union["DirectSecretAvailability", "GrantedSecretAvailability"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_secret_availability_type_0 = (
                    DirectSecretAvailability.from_dict(data)
                )

                return componentsschemas_secret_availability_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_secret_availability_type_1 = (
                GrantedSecretAvailability.from_dict(data)
            )

            return componentsschemas_secret_availability_type_1

        availability = _parse_availability(d.pop("availability"))

        project_secret_access = cls(
            secret=secret,
            availability=availability,
        )

        return project_secret_access
