from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
)

from attrs import define as _attrs_define

from ..models.compiled_profile_subagent_type import (
    CompiledProfileSubagentType,
    check_compiled_profile_subagent_type,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.compiled_subagent_model import CompiledSubagentModel


T = TypeVar("T", bound="CompiledProfileSubagent")


@_attrs_define
class CompiledProfileSubagent:
    """
    Attributes:
        type_ (CompiledProfileSubagentType):
        profile_id (str):
        description (Union[Unset, str]):
        model (Union[Unset, CompiledSubagentModel]):
        instruction_append (Union[Unset, str]):
        max_instances (Union[Unset, int]):
        archive_after_idle_minutes (Union[Unset, int]):
    """

    type_: CompiledProfileSubagentType
    profile_id: str
    description: Union[Unset, str] = UNSET
    model: Union[Unset, "CompiledSubagentModel"] = UNSET
    instruction_append: Union[Unset, str] = UNSET
    max_instances: Union[Unset, int] = UNSET
    archive_after_idle_minutes: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        profile_id = self.profile_id

        description = self.description

        model: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.model, Unset):
            model = self.model.to_dict()

        instruction_append = self.instruction_append

        max_instances = self.max_instances

        archive_after_idle_minutes = self.archive_after_idle_minutes

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "profile_id": profile_id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if model is not UNSET:
            field_dict["model"] = model
        if instruction_append is not UNSET:
            field_dict["instruction_append"] = instruction_append
        if max_instances is not UNSET:
            field_dict["max_instances"] = max_instances
        if archive_after_idle_minutes is not UNSET:
            field_dict["archive_after_idle_minutes"] = archive_after_idle_minutes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.compiled_subagent_model import CompiledSubagentModel

        d = dict(src_dict)
        type_ = check_compiled_profile_subagent_type(d.pop("type"))

        profile_id = d.pop("profile_id")

        description = d.pop("description", UNSET)

        _model = d.pop("model", UNSET)
        model: Union[Unset, CompiledSubagentModel]
        if isinstance(_model, Unset):
            model = UNSET
        else:
            model = CompiledSubagentModel.from_dict(_model)

        instruction_append = d.pop("instruction_append", UNSET)

        max_instances = d.pop("max_instances", UNSET)

        archive_after_idle_minutes = d.pop("archive_after_idle_minutes", UNSET)

        compiled_profile_subagent = cls(
            type_=type_,
            profile_id=profile_id,
            description=description,
            model=model,
            instruction_append=instruction_append,
            max_instances=max_instances,
            archive_after_idle_minutes=archive_after_idle_minutes,
        )

        return compiled_profile_subagent
