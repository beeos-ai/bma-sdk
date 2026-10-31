from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.interaction_form_context_item import InteractionFormContextItem
    from ..models.interaction_form_question import InteractionFormQuestion


T = TypeVar("T", bound="InteractionForm")


@_attrs_define
class InteractionForm:
    """
    Attributes:
        title (str):
        questions (list['InteractionFormQuestion']):
        context (Union[Unset, list['InteractionFormContextItem']]):
    """

    title: str
    questions: list["InteractionFormQuestion"]
    context: Union[Unset, list["InteractionFormContextItem"]] = UNSET

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        questions = []
        for questions_item_data in self.questions:
            questions_item = questions_item_data.to_dict()
            questions.append(questions_item)

        context: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.context, Unset):
            context = []
            for context_item_data in self.context:
                context_item = context_item_data.to_dict()
                context.append(context_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "title": title,
                "questions": questions,
            }
        )
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.interaction_form_context_item import InteractionFormContextItem
        from ..models.interaction_form_question import InteractionFormQuestion

        d = dict(src_dict)
        title = d.pop("title")

        questions = []
        _questions = d.pop("questions")
        for questions_item_data in _questions:
            questions_item = InteractionFormQuestion.from_dict(questions_item_data)

            questions.append(questions_item)

        context = []
        _context = d.pop("context", UNSET)
        for context_item_data in _context or []:
            context_item = InteractionFormContextItem.from_dict(context_item_data)

            context.append(context_item)

        interaction_form = cls(
            title=title,
            questions=questions,
            context=context,
        )

        return interaction_form
