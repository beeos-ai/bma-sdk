"""Python template of tools/sdkgen/sdkgen.py (ADR 0012, Lead decision D4).

Writes, per contract surface (rest | facade):

- models.py       pydantic v2 response models, one per object schema
                       (inline objects named <Parent><Property>), Literal
                       enums, discriminated unions annotated with
                       PropertyInfo(discriminator=...), and the event classes
                       of every text/event-stream operation;
- params.py       TypedDict request types (<Schema>Param) for every
                       schema that contains an object or a timestamp;
- operations.py one OperationDescriptor per mapped operation;
- resources.py    sync and async resource classes whose methods take
                       path IDs positionally and the flattened query, header
                       and body fields as keyword arguments.

Response models are built without validation (bma_sdk._models.construct,
after the Stainless SDKs), so a field the server adds or an enum value the
contract marks extensible does not break an older client.
"""
from __future__ import annotations

import json
import keyword
import re
from dataclasses import dataclass, field
from typing import Any

PY_RESERVED_FIELDS = {"model_config", "model_fields", "model_extra", "construct", "copy", "dict", "json", "schema"}
OPTION_KWARGS = {"extra_headers", "extra_query", "extra_body", "timeout"}


class PyGenError(Exception):
    pass


def pascal(name: str) -> str:
    parts = re.split(r"[_\-\s.]+", name)
    return "".join(p[:1].upper() + p[1:] for p in parts if p)


def snake(name: str) -> str:
    for word, repl in (("GitHub", "Github"), ("OAuth", "Oauth"), ("MCP", "Mcp"), ("BYO", "Byo"), ("API", "Api")):
        name = name.replace(word, repl)
    name = re.sub(r"ID$", "Id", name)
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def doc_literal(text: str, indent: str) -> list[str]:
    text = text.strip().replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    if not text:
        return []
    lines = text.splitlines()
    if len(lines) == 1:
        return [f'{indent}"""{lines[0]}"""']
    return [f'{indent}"""{lines[0]}'] + [f"{indent}{l}" if l else "" for l in lines[1:]] + [f'{indent}"""']


def pylit(value: Any) -> str:
    return json.dumps(value) if isinstance(value, str) else repr(value)


@dataclass
class PyField:
    name: str
    type: str
    required: bool
    description: str = ""


@dataclass
class PyClass:
    name: str
    fields: list[PyField]
    description: str = ""
    key: str = ""  # identity of the defining schema node


@dataclass
class Types:
    """Python type expressions for the schemas of one contract, in one mode."""

    doc: dict[str, Any]
    mode: str  # model | param
    models_module_names: set[str] = field(default_factory=set)  # param mode: names imported from models
    classes: dict[str, PyClass] = field(default_factory=dict)
    aliases: dict[str, str] = field(default_factory=dict)
    alias_docs: dict[str, str] = field(default_factory=dict)
    _plain: dict[str, bool] = field(default_factory=dict)

    @property
    def schemas(self) -> dict[str, Any]:
        return self.doc.get("components", {}).get("schemas", {})

    def deref(self, node: Any) -> Any:
        while isinstance(node, dict) and "$ref" in node:
            target: Any = self.doc
            for part in node["$ref"].removeprefix("#/").split("/"):
                target = target[part]
            node = target
        return node

    # -- classification ---------------------------------------------------

    def typed(self, node: Any) -> bool:
        """Whether a schema node constrains the type (not only validation)."""
        if not isinstance(node, dict):
            return False
        if any(k in node for k in ("$ref", "type", "properties", "const", "enum", "items")):
            return True
        for k in ("oneOf", "anyOf", "allOf"):
            if any(self.typed(b) for b in node.get(k, [])):
                return True
        return False

    def plain(self, name: str) -> bool:
        """A schema whose param type equals its model type (no object, no timestamp)."""
        if name not in self._plain:
            self._plain[name] = True  # cycle guard: recursive schemas contain objects anyway
            self._plain[name] = not self._needs_param(self.schemas[name], set())
        return self._plain[name]

    def _needs_param(self, node: Any, seen: set[str]) -> bool:
        if isinstance(node, list):
            return any(self._needs_param(n, seen) for n in node)
        if not isinstance(node, dict):
            return False
        if "$ref" in node:
            name = node["$ref"].split("/")[-1]
            if name in seen:
                return True
            return self._needs_param(self.schemas[name], seen | {name})
        if "properties" in node or node.get("format") in ("date-time", "binary"):
            return True
        t = node.get("type")
        if t == "object" or (isinstance(t, list) and "object" in t):
            ap = node.get("additionalProperties")
            if isinstance(ap, dict) and self.typed(ap):
                return self._needs_param(ap, seen)
            return False
        return any(self._needs_param(node.get(k), seen) for k in ("items", "oneOf", "anyOf", "allOf"))

    # -- names ------------------------------------------------------------

    def ref_name(self, name: str) -> str:
        if self.mode == "param":
            if self.plain(name):
                self.models_module_names.add(name)
                return name
            self.schema_type(name)
            return name + "Param"
        self.schema_type(name)
        return name

    def class_name(self, base: str) -> str:
        return base + "Param" if self.mode == "param" else base

    # -- top-level schemas --------------------------------------------------

    def schema_type(self, name: str) -> None:
        """Defines the class or alias of a component schema."""
        out = self.class_name(name)
        if out in self.classes or out in self.aliases:
            return
        node = self.schemas[name]
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            raise PyGenError(f"schema name {name} is not a Python identifier")
        if self.is_object(node):
            self.classes[out] = PyClass(out, [], key=f"#/components/schemas/{name}")  # placeholder for recursion
            self.classes[out] = self.object_class(out, node)
        else:
            self.aliases[out] = "object"  # placeholder for recursion
            self.aliases[out] = self.expr(node, name)
            if node.get("description"):
                self.alias_docs[out] = node["description"]

    def is_object(self, node: dict[str, Any]) -> bool:
        if "properties" in node:
            return True
        all_of = node.get("allOf", [])
        if all_of and len([b for b in all_of if self.typed(b)]) > 1:
            return True
        if all_of and any("properties" in self.deref(b) for b in all_of) and len(all_of) > 1:
            return True
        if all_of and len(all_of) == 1 and "unevaluatedProperties" in node:
            return True  # MachineSummary: allOf [Fields] closed — a class of its own
        return False

    # -- objects ------------------------------------------------------------

    def collect(self, node: Any) -> tuple[dict[str, list[Any]], set[str], bool]:
        """Properties (possibly several schemas each), required names, and
        whether the object is open (additional properties allowed)."""
        node = self.deref(node)
        props: dict[str, list[Any]] = {}
        required: set[str] = set()
        for k, v in (node.get("properties") or {}).items():
            props.setdefault(k, []).append(v)
        if "properties" in node:
            required |= set(node.get("required") or [])
        for part in node.get("allOf", []):
            if not self.typed(part):
                continue
            p, r, _ = self.collect(part)
            for k, v in p.items():
                props.setdefault(k, []).extend(v)
            required |= r
        if "properties" not in node:
            branches = [b for b in node.get("oneOf", []) + node.get("anyOf", []) if self.typed(b) and self.deref(b).get("type") != "null"]
            if branches:
                common: set[str] | None = None
                for b in branches:
                    p, r, _ = self.collect(b)
                    for k, v in p.items():
                        props.setdefault(k, []).extend(v)
                    common = r if common is None else common & r
                required |= common or set()
        return props, required, node.get("additionalProperties") is not False

    def object_class(self, name: str, node: dict[str, Any]) -> PyClass:
        props, required, _ = self.collect(node)
        fields = []
        for prop, schemas in props.items():
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", prop) or keyword.iskeyword(prop) or prop in PY_RESERVED_FIELDS:
                raise PyGenError(f"{name}.{prop} is not a usable Python field name")
            exprs = list(dict.fromkeys(self.expr(s, name.removesuffix("Param") + pascal(prop)) for s in schemas))
            t = exprs[0] if len(exprs) == 1 else f"Union[{', '.join(exprs)}]"
            desc = next((self.deref(s).get("description") or s.get("description") for s in schemas if isinstance(s, dict) and (s.get("description") or self.deref(s).get("description"))), "")
            if "$ref" in schemas[0] and not schemas[0].get("description"):
                desc = ""  # the referenced schema carries its own docs
            fields.append(PyField(prop, t, prop in required, desc or ""))
        return PyClass(name, fields, node.get("description", ""))

    def inline_class(self, base: str, node: dict[str, Any]) -> str:
        name = self.class_name(base)
        key = json.dumps(node, sort_keys=True)
        existing = self.classes.get(name)
        if existing is not None:
            if existing.key != key:
                raise PyGenError(f"inline schema name {name} collides with another definition")
            return name
        if name in self.aliases or (self.mode == "model" and base in self.schemas):
            raise PyGenError(f"inline schema name {name} collides with a component schema")
        self.classes[name] = PyClass(name, [], key=key)
        cls = self.object_class(name, node)
        cls.key = key
        self.classes[name] = cls
        return name

    # -- expressions ----------------------------------------------------------

    def expr(self, node: Any, ctx: str) -> str:
        """Python type expression of a schema node; ctx names inline classes."""
        if not isinstance(node, dict) or not node:
            return "object"
        if "$ref" in node:
            return self.ref_name(node["$ref"].split("/")[-1])
        if "const" in node:
            return f"Literal[{pylit(node['const'])}]"
        if "enum" in node:
            values = [v for v in node["enum"] if v is not None]
            lit = f"Literal[{', '.join(pylit(v) for v in values)}]"
            if node.get("x-extensible-enum"):
                lit = f"Union[{lit}, str]"
            return f"Optional[{lit}]" if None in node["enum"] else lit
        if self.is_object(node):
            return self.inline_class(ctx, node)
        for key in ("oneOf", "anyOf"):
            branches = [b for b in node.get(key, []) if self.typed(b)]
            if branches:
                return self.union(node, branches, ctx)
        all_of = [b for b in node.get("allOf", []) if self.typed(b)]
        if len(all_of) == 1 and "type" not in node:
            return self.expr(all_of[0], ctx)
        t = node.get("type")
        if isinstance(t, list):
            non_null = [x for x in t if x != "null"]
            inner = [self.expr({**node, "type": x}, ctx) for x in non_null]
            out = inner[0] if len(inner) == 1 else f"Union[{', '.join(inner)}]"
            return f"Optional[{out}]" if "null" in t else out
        if t == "object":
            ap = node.get("additionalProperties")
            if isinstance(ap, dict) and self.typed(ap):
                return f"Dict[str, {self.expr(ap, ctx + 'Value')}]"
            return "Dict[str, object]"
        if t == "array":
            return f"List[{self.expr(node.get('items') or {}, ctx + 'Item')}]"
        if t == "string":
            fmt = node.get("format")
            if fmt == "date-time":
                return "Union[str, datetime]" if self.mode == "param" else "datetime"
            if fmt == "binary":
                return "FileTypes" if self.mode == "param" else "bytes"
            return "str"
        if t == "integer":
            return "int"
        if t == "number":
            return "float"
        if t == "boolean":
            return "bool"
        if t == "null":
            return "None"
        return "object"

    def union(self, node: dict[str, Any], branches: list[Any], ctx: str) -> str:
        nullable = any(self.deref(b).get("type") == "null" for b in branches)
        typed = [b for b in branches if self.deref(b).get("type") != "null"]
        objects = [b for b in typed if "$ref" not in b and self.is_object(b)]
        exprs = []
        for b in typed:
            sub = ctx + (f"Variant{objects.index(b)}" if b in objects and len(objects) > 1 else "")
            exprs.append(self.expr(b, sub))
        exprs = list(dict.fromkeys(exprs))
        if not exprs:
            return "None"
        out = exprs[0] if len(exprs) == 1 else f"Union[{', '.join(exprs)}]"
        disc = (node.get("discriminator") or {}).get("propertyName")
        if disc and self.mode == "model" and len(exprs) > 1:
            out = f'Annotated[{out}, PropertyInfo(discriminator="{disc}")]'
        return f"Optional[{out}]" if nullable else out

    # -- rendering ------------------------------------------------------------

    def ordered_aliases(self) -> list[str]:
        """Aliases after the classes, each after the aliases it uses."""
        order: list[str] = []
        state: dict[str, int] = {}

        def visit(name: str, stack: tuple[str, ...]) -> None:
            if state.get(name) == 2:
                return
            if state.get(name) == 1:
                raise PyGenError(f"recursive type alias {' -> '.join(stack + (name,))}")
            state[name] = 1
            for dep in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", self.aliases[name]):
                if dep in self.aliases and dep != name:
                    visit(dep, stack + (name,))
            state[name] = 2
            order.append(name)

        for name in sorted(self.aliases):
            visit(name, ())
        return order


HEADER = [
    "# Code generated by tools/sdkgen/sdkgen.py from the contract and",
    "# contracts/bma/sdk.resources.yaml; DO NOT EDIT.",
]


def render_models(types: Types, extra_classes: list[PyClass], extra_aliases: dict[str, str]) -> str:
    out = HEADER + [
        "# pyright: reportUnusedImport=false",
        "from __future__ import annotations",
        "",
        "from datetime import datetime",
        "from typing import Dict, List, Optional, Union",
        "",
        "from typing_extensions import Annotated, Literal, TypeAlias",
        "",
        "from ..._models import BaseModel, PropertyInfo",
        "",
    ]
    classes = sorted(types.classes.values(), key=lambda c: c.name) + extra_classes
    names = [c.name for c in classes] + types.ordered_aliases() + list(extra_aliases)
    out.append("__all__ = [")
    out += [f'    "{n}",' for n in names]
    out.append("]")
    for c in classes:
        out += ["", ""]
        out.append(f"class {c.name}(BaseModel):")
        body = doc_literal(c.description, "    ")
        for f in c.fields:
            if body:
                body.append("")
            t = f.type if f.required else (f.type if f.type.startswith("Optional[") else f"Optional[{f.type}]")
            body.append(f"    {f.name}: {t}" + ("" if f.required else " = None"))
            body += doc_literal(f.description, "    ")
        out += body or ["    pass"]
    out.append("")
    for name in types.ordered_aliases():
        out.append("")
        out.append(f"{name}: TypeAlias = {types.aliases[name]}")
        out += doc_literal(types.alias_docs.get(name, ""), "")
    for name, value in extra_aliases.items():
        out.append("")
        out.append(f"{name}: TypeAlias = {value}")
    return "\n".join(out) + "\n"


def render_params(types: Types, models_module: str) -> str:
    out = HEADER + [
        "# pyright: reportUnusedImport=false",
        "from __future__ import annotations",
        "",
        "from datetime import datetime",
        "from typing import Dict, List, Optional, Union",
        "",
        "from typing_extensions import Literal, Required, TypeAlias, TypedDict",
        "",
        "from ..._types import FileTypes",
    ]
    imported = sorted(types.models_module_names)
    if imported:
        out.append(f"from .{models_module} import (")
        out += [f"    {n}," for n in imported]
        out.append(")")
    classes = sorted(types.classes.values(), key=lambda c: c.name)
    out.append("")
    out.append("__all__ = [")
    out += [f'    "{n}",' for n in [c.name for c in classes] + types.ordered_aliases()]
    out.append("]")
    for c in classes:
        out += ["", ""]
        out.append(f"class {c.name}(TypedDict, total=False):")
        body = doc_literal(c.description, "    ")
        for f in c.fields:
            if body:
                body.append("")
            body.append(f"    {f.name}: " + (f"Required[{f.type}]" if f.required else f.type))
            body += doc_literal(f.description, "    ")
        out += body or ["    pass"]
    out.append("")
    for name in types.ordered_aliases():
        out.append("")
        out.append(f"{name}: TypeAlias = {types.aliases[name]}")
    return "\n".join(out) + "\n"


# --- resources -------------------------------------------------------------


@dataclass
class Kwarg:
    name: str
    type: str
    required: bool
    nullable: bool = False


class PythonResources:
    def __init__(self, contract: Any, roots: list[Any], section: str, base: str, root: str, mixins: dict[str, tuple[str, str]]):
        self.contract = contract
        self.roots = roots
        self.section = section
        self.base = base  # file prefix, e.g. rest
        self.root = root  # Rest | Facade
        self.mixins = mixins
        self.models = Types(contract.doc, "model")
        self.params = Types(contract.doc, "param")
        self.event_classes: list[PyClass] = []
        self.event_aliases: dict[str, str] = {}
        self.event_maps: dict[str, list[tuple[str, str]]] = {}

    def walk(self):
        def rec(rs):
            for r in rs:
                yield from rec(r.children)
                yield r
        return list(rec(self.roots))

    # Every component schema gets a model, so the types module is complete
    # even for schemas only reachable from unmapped operations.
    def define_all(self) -> None:
        for name in self.models.schemas:
            self.models.schema_type(name)
            if not self.params.plain(name):
                self.params.schema_type(name)

    def body_schema(self, op_raw: dict[str, Any], kind: str) -> tuple[Any, str]:
        content = self.contract.deref(op_raw["requestBody"])["content"]
        media = "application/json" if kind == "json" else "multipart/form-data"
        schema = content[media]["schema"]
        ctx = schema["$ref"].split("/")[-1] if "$ref" in schema else pascal(op_raw["operationId"]) + "Body"
        return schema, ctx

    def raw(self, op: Any) -> dict[str, Any]:
        return self.contract.doc["paths"][op.path][op.method.lower()]

    def kwargs(self, m: Any) -> list[Kwarg]:
        op = m.op
        raw = self.raw(op)
        out: list[Kwarg] = []
        positional = {snake(p.name) for p in m.positional}
        for p in op.params:
            if p.location == "path":
                if p.scope and p not in m.positional:
                    out.append(Kwarg(p.key, "str", False))
                continue
            if p.scope:  # x-bma-project-id header
                out.append(Kwarg(p.key, "str", False))
                continue
            node = self.contract.deref(next(
                x for x in self.contract.doc["paths"][op.path].get("parameters", []) + raw.get("parameters", [])
                if self.contract.deref(x)["name"] == p.name and self.contract.deref(x)["in"] == p.location
            ))
            schema = node.get("schema") or {}
            t = self.params.expr(schema, pascal(op.op_id) + pascal(p.key))
            if p.location == "query" and t.startswith("Optional["):
                t = t[len("Optional["):-1]
            out.append(Kwarg(p.key, t, p.required))
        if op.body_kind in ("json", "multipart"):
            schema, ctx = self.body_schema(raw, op.body_kind)
            props, required, _ = self.params.collect(schema)
            for prop, schemas in props.items():
                exprs = list(dict.fromkeys(self.params.expr(s, ctx + pascal(prop)) for s in schemas))
                t = exprs[0] if len(exprs) == 1 else f"Union[{', '.join(exprs)}]"
                out.append(Kwarg(prop, t, op.body_required and prop in required))
        elif op.body_kind == "binary":
            out.append(Kwarg("body", "Union[bytes, str, IO[bytes]]", op.body_required))
        names = [k.name for k in out]
        for k in out:
            if names.count(k.name) > 1:
                raise PyGenError(f"{op.op_id}: parameter {k.name} appears twice")
            if k.name in positional:
                raise PyGenError(f"{op.op_id}: parameter {k.name} collides with a positional argument")
            if k.name in OPTION_KWARGS or (op.idempotency and k.name == "idempotency_key"):
                raise PyGenError(f"{op.op_id}: parameter {k.name} collides with a request option")
            if keyword.iskeyword(k.name) or not k.name.isidentifier():
                raise PyGenError(f"{op.op_id}: parameter {k.name} is not a Python identifier")
        return out

    def response(self, op: Any) -> str:
        if op.response_kind == "void":
            return "None"
        if op.response_kind == "binary":
            return "httpx.Response"
        raw = self.raw(op)
        types = []
        for code in op.response_codes:
            schema = self.contract.deref(raw["responses"][str(code)])["content"]["application/json"]["schema"]
            types.append(self.models.expr(schema, pascal(op.op_id) + "Response"))
        types = list(dict.fromkeys(types))
        return types[0] if len(types) == 1 else f"Union[{', '.join(types)}]"

    def page_item(self, op: Any) -> str:
        raw = self.raw(op)
        schema = self.contract.deref(self.contract.deref(raw["responses"]["200"])["content"]["application/json"]["schema"])
        items = self.contract.deref(schema["properties"]["data"]).get("items") or {}
        return self.models.expr(items, pascal(op.op_id) + "ResponseDataItem")

    def events(self, op: Any) -> str:
        name = pascal(op.op_id) + "Event"
        if name not in self.event_aliases:
            members = []
            mapping = []
            for e in op.sse_events:
                if e["event"] == "error":
                    continue
                cls = name + pascal(e["event"])
                fields = [PyField("event", f'Literal["{e["event"]}"]', True)]
                if e["durable"]:
                    fields += [PyField("id", "str", True), PyField("sequence", "int", True)]
                fields.append(PyField("data", self.models.ref_name(e["schema"]), True))
                self.event_classes.append(PyClass(cls, fields, f"`{e['event']}` frame of {op.op_id}."))
                members.append(cls)
                mapping.append((e["event"], cls))
            self.event_aliases[name] = f"Union[{', '.join(members)}]"
            self.event_maps[name] = mapping
        return name

    def descriptor(self, op: Any) -> str:
        d: list[str] = [f'id="{op.op_id}"', f'method="{op.method}"', f'path="{op.path}"']
        path = {p.name: p.key for p in op.params if p.location == "path"}
        if path:
            d.append(f"path_params={json.dumps(path)}")
        query = {p.name: p.style for p in op.params if p.location == "query"}
        if query:
            d.append(f"query={json.dumps(query)}")
        headers = {p.name: p.key for p in op.params if p.location == "header"}
        if headers:
            d.append(f"headers={json.dumps(headers)}")
        if op.body_kind:
            d.append(f'body="{op.body_kind}"')
            if op.body_required:
                d.append("body_required=True")
        if op.multipart_json:
            d.append(f"multipart_json={tuple(op.multipart_json)!r}")
        if op.multipart_files:
            d.append(f"multipart_files={tuple(op.multipart_files)!r}")
        d.append(f'response="{op.response_kind}"')
        if op.idempotency:
            d.append("idempotency=True")
        if op.page:
            d.append(f"page={tuple(tuple(pair) for pair in op.page)!r}")
        return f"OperationDescriptor({', '.join(d)})"

    def render_operations(self) -> str:
        ops = sorted({m.op.op_id: m.op for r in self.walk() for m in r.methods}.values(), key=lambda o: o.op_id)
        out = HEADER + ["from ..._core import OperationDescriptor", ""]
        for op in ops:
            out.append(f"{op.op_id} = {self.descriptor(op)}")
        return "\n".join(out) + "\n"

    def method(self, m: Any, is_async: bool) -> list[str]:
        op = m.op
        name = snake(m.name)
        kwargs = self.kwargs(m)
        args = ["self"] + [f"{snake(p.name)}: str" for p in m.positional]
        if kwargs or True:
            args.append("*")
        for k in sorted(kwargs, key=lambda k: not k.required):
            if k.required:
                args.append(f"{k.name}: {k.type}")
            else:
                args.append(f"{k.name}: Union[{k.type}, NotGiven] = NOT_GIVEN")
        if op.idempotency:
            args.append("idempotency_key: Optional[str] = None")
        args += [
            "extra_headers: Optional[Headers] = None",
            "extra_query: Optional[Query] = None",
            "timeout: Union[Timeout, NotGiven] = NOT_GIVEN",
        ]
        path = "{" + ", ".join(f'"{p.name}": {snake(p.name)}' for p in m.positional) + "}"
        params = "{" + ", ".join(f'"{k.name}": {k.name}' for k in kwargs) + "}"
        opts = "RequestOptions(extra_headers=extra_headers, extra_query=extra_query, timeout=timeout" + (
            ", idempotency_key=idempotency_key)" if op.idempotency else ")"
        )
        call_args = f"_ops.{op.op_id}, {path}, {params}, {opts}"
        doc = f'        """`{op.method} {op.path}` ({op.op_id})."""'
        aw = "await " if is_async else ""
        df = "async def" if is_async else "def"
        if op.response_kind == "sse":
            ev = self.events(op)
            stream = "AsyncStream" if is_async else "Stream"
            return [
                f"    def {name}({', '.join(args)}) -> {stream}[{ev}]:",
                doc,
                f"        return self._client._stream({call_args}, _models.{ev}_EVENTS)",
            ]
        if op.paginated:
            item = self.page_item(op)
            ret = f"AsyncPaginator[{item}]" if is_async else f"SyncCursorPage[{item}]"
            return [
                f"    def {name}({', '.join(args)}) -> {ret}:",
                doc,
                f"        return self._client._page({call_args}, {item})",
            ]
        resp = self.response(op)
        return [
            f"    {df} {name}({', '.join(args)}) -> {resp}:",
            doc,
            f"        return {aw}self._client._request({call_args}, {resp})",
        ]

    def qualify(self, text: str) -> str:
        """Prefixes generated type names with their module; idempotent."""
        params = set(self.params.classes) | set(self.params.aliases)
        models = set(self.models.classes) | set(self.models.aliases) | set(self.event_aliases)

        def sub(mt: re.Match[str]) -> str:
            w = mt[0]
            if w in params:
                return f"_params.{w}"
            if w in models:
                return f"_models.{w}"
            return w

        return re.sub(r"(?<![.\w])[A-Za-z_][A-Za-z0-9_]*", sub, text)

    def render_resources(self) -> str:
        self.define_all()
        body: list[str] = []
        for is_async in (False, True):
            prefix = "Async" if is_async else ""
            base_res = "AsyncAPIResource" if is_async else "SyncAPIResource"
            for r in self.walk():
                cls = prefix + r.class_name
                base = base_res
                if r.class_name in self.mixins:
                    base = prefix + self.mixins[r.class_name][1]
                body += ["", ""]
                body.append(f"class {cls}({base}):")
                lines: list[str] = []
                for c in r.children:
                    lines += [
                        "    @cached_property",
                        f"    def {snake(c.name)}(self) -> {prefix}{c.class_name}:",
                        f"        return {prefix}{c.class_name}(self._client)",
                        "",
                    ]
                for m in r.methods:
                    lines += [self.qualify(line) for line in self.method(m, is_async)] + [""]
                body += (lines[:-1] if lines else ["    pass"])
            body += ["", ""]
            core = "AsyncClientCore" if is_async else "SyncClientCore"
            body.append(f"class {prefix}{self.root}ClientBase({core}):")
            body.append(f'    """Top-level resources of the {self.section} API."""')
            for r in self.roots:
                body += [
                    "",
                    "    @cached_property",
                    f"    def {snake(r.name)}(self) -> {prefix}{r.class_name}:",
                    f"        return {prefix}{r.class_name}(self)",
                ]
        imports = HEADER + [
            "# pyright: reportUnusedImport=false",
            "from __future__ import annotations",
            "",
            "from datetime import datetime",
            "from functools import cached_property",
            "from typing import IO, Dict, List, Optional, Union",
            "",
            "import httpx",
            "from typing_extensions import Literal",
            "",
            "from ..._core import AsyncClientCore, RequestOptions, SyncClientCore, Timeout",
            "from ..._pagination import AsyncPaginator, SyncCursorPage",
            "from ..._resource import AsyncAPIResource, SyncAPIResource",
            "from ..._streaming import AsyncStream, Stream",
            "from ..._types import NOT_GIVEN, FileTypes, Headers, NotGiven, Query",
            "from . import models as _models",
            "from . import operations as _ops",
            "from . import params as _params",
        ]
        for name in sorted({r.class_name for r in self.walk() if r.class_name in self.mixins}):
            module, base = self.mixins[name]
            imports.append(f"from {module} import Async{base}, {base}")
        return "\n".join(imports + body) + "\n"

    def render_models(self) -> str:
        extra_aliases = dict(self.event_aliases)
        out = render_models(self.models, self.event_classes, extra_aliases)
        lines = [out.rstrip("\n"), ""]
        for name, mapping in self.event_maps.items():
            lines.append("")
            lines.append(f"{name}_EVENTS: Dict[str, type[BaseModel]] = {{")
            lines += [f'    "{ev}": {cls},' for ev, cls in mapping]
            lines.append("}")
            lines.append(f'"""Event class of each SSE event name of {name}."""')
        return "\n".join(lines) + "\n"

    def render_params(self) -> str:
        return render_params(self.params, "models")
