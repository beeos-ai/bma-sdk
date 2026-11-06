"""Base class of the response models and their non-validating construction.

Responses are built the way the Stainless SDKs (anthropic, openai) build
them: guided by the type annotations but without validation, so a field the
server adds, or a new value of an extensible enum, never breaks an older
client. Discriminated unions pick their member by the discriminator value.
"""

from __future__ import annotations

import inspect
import sys
import types
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Union, cast, get_args, get_origin, get_type_hints

import pydantic
from pydantic import ConfigDict
from typing_extensions import Annotated, Literal, Self

__all__ = ["BaseModel", "PropertyInfo", "construct"]

_DATETIME = pydantic.TypeAdapter(datetime)


class PropertyInfo:
    """Annotated metadata: the union is discriminated by this property."""

    def __init__(self, *, discriminator: str) -> None:
        self.discriminator = discriminator


class BaseModel(pydantic.BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra="allow",
        defer_build=True,
        protected_namespaces=(),
        arbitrary_types_allowed=True,
    )

    @classmethod
    def construct_from(cls, data: object) -> Self:
        """Builds the model from decoded JSON without validation."""
        return cast(Self, construct(cls, data))

    def to_dict(self) -> Dict[str, object]:
        """The fields the server sent, as JSON-compatible values."""
        return self.model_dump(mode="json", exclude_unset=True, warnings=False)

    def to_json(self, *, indent: int | None = 2) -> str:
        return self.model_dump_json(indent=indent, exclude_unset=True, warnings=False)


_HINTS: dict[type, dict[str, Any]] = {}
_VARIANTS: dict[tuple[Any, str], dict[object, type]] = {}


def _hints(cls: type[BaseModel]) -> dict[str, Any]:
    hints = _HINTS.get(cls)
    if hints is None:
        # Own annotations only: the generated models do not inherit fields,
        # and pydantic's own annotations need not resolve here.
        holder = types.SimpleNamespace(__annotations__=inspect.get_annotations(cls))
        hints = get_type_hints(holder, globalns=vars(sys.modules[cls.__module__]), include_extras=True)
        _HINTS[cls] = hints
    return hints


def construct(tp: Any, value: object) -> Any:
    """Builds ``value`` (decoded JSON) as type ``tp`` without validation.
    Values that do not fit the annotation are kept as they are."""
    if value is None:
        return None
    origin = get_origin(tp)
    if origin is Annotated:
        base, *meta = get_args(tp)
        info = next((m for m in meta if isinstance(m, PropertyInfo)), None)
        if info is not None and isinstance(value, dict):
            variant = _variants(base, info.discriminator).get(cast(Dict[str, object], value).get(info.discriminator))
            if variant is not None:
                return construct(variant, value)
        return construct(base, value)
    if origin in (Union, types.UnionType):
        members = [a for a in get_args(tp) if a is not type(None)]
        for member in members:
            if _fits(member, value):
                return construct(member, value)
        return value
    if origin is Literal:
        return value
    if origin in (list, List):
        if not isinstance(value, list):
            return value
        (item,) = get_args(tp) or (object,)
        return [construct(item, v) for v in cast(List[object], value)]
    if origin in (dict, Dict):
        if not isinstance(value, dict):
            return value
        args = get_args(tp)
        item = args[1] if len(args) == 2 else object
        return {k: construct(item, v) for k, v in cast(Dict[str, object], value).items()}
    if isinstance(tp, type) and issubclass(tp, BaseModel):
        if not isinstance(value, dict):
            return value
        return _construct_model(tp, cast(Dict[str, object], value))
    if tp is datetime and isinstance(value, str):
        try:
            return _DATETIME.validate_python(value)
        except pydantic.ValidationError:
            return value
    return value


def _construct_model(cls: type[BaseModel], data: dict[str, object]) -> BaseModel:
    hints = _hints(cls)
    fields: dict[str, object] = {}
    for name in cls.model_fields:
        if name in data:
            fields[name] = construct(hints.get(name, object), data[name])
    extra = {k: v for k, v in data.items() if k not in cls.model_fields}
    return cls.model_construct(_fields_set=set(fields) | set(extra), **fields, **extra)


def _variants(union: Any, prop: str) -> dict[object, type]:
    key = (union, prop)
    found = _VARIANTS.get(key)
    if found is None:
        found = {}
        for member in get_args(union):
            if isinstance(member, type) and issubclass(member, BaseModel):
                hint = _hints(member).get(prop)
                if get_origin(hint) is Literal:
                    for v in get_args(hint):
                        found.setdefault(v, member)
        _VARIANTS[key] = found
    return found


def _fits(tp: Any, value: object) -> bool:
    """Whether a plain union member plausibly describes ``value``."""
    origin = get_origin(tp)
    if origin is Annotated:
        return _fits(get_args(tp)[0], value)
    if origin in (Union, types.UnionType):
        return any(_fits(a, value) for a in get_args(tp))
    if origin is Literal:
        return value in get_args(tp)
    if origin in (list, List):
        return isinstance(value, list)
    if origin in (dict, Dict):
        return isinstance(value, dict)
    if isinstance(tp, type) and issubclass(tp, BaseModel):
        if not isinstance(value, dict):
            return False
        data = cast(Dict[str, object], value)
        hints = _hints(tp)
        for name, field in tp.model_fields.items():
            if field.is_required() and name not in data:
                return False
            hint = hints.get(name)
            if name in data and get_origin(hint) is Literal and data[name] not in get_args(hint):
                return False
        return True
    if tp is bool:
        return isinstance(value, bool)
    if tp is int:
        return isinstance(value, int) and not isinstance(value, bool)
    if tp is float:
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if tp in (str, datetime):
        return isinstance(value, str)
    if tp is bytes:
        return isinstance(value, (bytes, str))
    if tp is type(None):
        return value is None
    return True
