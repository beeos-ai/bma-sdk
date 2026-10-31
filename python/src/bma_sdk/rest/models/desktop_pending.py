import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)
from uuid import UUID

from attrs import define as _attrs_define
from dateutil.parser import isoparse

T = TypeVar("T", bound="DesktopPending")


@_attrs_define
class DesktopPending:
    """
    Attributes:
        id (UUID):
        generation (int):
        seq (int):
        submitted_at (datetime.datetime):
    """

    id: UUID
    generation: int
    seq: int
    submitted_at: datetime.datetime

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        generation = self.generation

        seq = self.seq

        submitted_at = self.submitted_at.isoformat()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "generation": generation,
                "seq": seq,
                "submitted_at": submitted_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        generation = d.pop("generation")

        seq = d.pop("seq")

        submitted_at = isoparse(d.pop("submitted_at"))

        desktop_pending = cls(
            id=id,
            generation=generation,
            seq=seq,
            submitted_at=submitted_at,
        )

        return desktop_pending
