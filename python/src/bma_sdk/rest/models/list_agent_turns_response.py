from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.agent_turn import AgentTurn


T = TypeVar("T", bound="ListAgentTurnsResponse")


@_attrs_define
class ListAgentTurnsResponse:
    """
    Attributes:
        data (list['AgentTurn']):
        next_before_turn_sequence (Union[None, int]): Pass this value as before_turn_sequence to fetch older turns, or
            null when this page reached the beginning of the agent's turns.
    """

    data: list["AgentTurn"]
    next_before_turn_sequence: Union[None, int]

    def to_dict(self) -> dict[str, Any]:
        data = []
        for data_item_data in self.data:
            data_item = data_item_data.to_dict()
            data.append(data_item)

        next_before_turn_sequence: Union[None, int]
        next_before_turn_sequence = self.next_before_turn_sequence

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "data": data,
                "next_before_turn_sequence": next_before_turn_sequence,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.agent_turn import AgentTurn

        d = dict(src_dict)
        data = []
        _data = d.pop("data")
        for data_item_data in _data:
            data_item = AgentTurn.from_dict(data_item_data)

            data.append(data_item)

        def _parse_next_before_turn_sequence(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        next_before_turn_sequence = _parse_next_before_turn_sequence(
            d.pop("next_before_turn_sequence")
        )

        list_agent_turns_response = cls(
            data=data,
            next_before_turn_sequence=next_before_turn_sequence,
        )

        return list_agent_turns_response
