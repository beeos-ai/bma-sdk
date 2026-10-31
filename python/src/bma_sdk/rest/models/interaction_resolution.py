from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.interaction_answer import InteractionAnswer


T = TypeVar("T", bound="InteractionResolution")


@_attrs_define
class InteractionResolution:
    """
    Attributes:
        answers (list['InteractionAnswer']): Answers in the same order as the interaction form's questions.
    """

    answers: list["InteractionAnswer"]

    def to_dict(self) -> dict[str, Any]:
        answers = []
        for answers_item_data in self.answers:
            answers_item = answers_item_data.to_dict()
            answers.append(answers_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "answers": answers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.interaction_answer import InteractionAnswer

        d = dict(src_dict)
        answers = []
        _answers = d.pop("answers")
        for answers_item_data in _answers:
            answers_item = InteractionAnswer.from_dict(answers_item_data)

            answers.append(answers_item)

        interaction_resolution = cls(
            answers=answers,
        )

        return interaction_resolution
