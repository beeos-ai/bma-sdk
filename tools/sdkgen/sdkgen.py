#!/usr/bin/env python3
"""Thin resource-layer generator for the bma-sdk clients (ADR 0012, D1).

Reads an OpenAPI document and the resource map in
contracts/bma/sdk.resources.yaml and writes the resource classes, request
descriptors and parameter types of one SDK surface. The schema types
themselves come from the language's existing type generator
(openapi-typescript for TypeScript); this script only adds the
resource-shaped methods on top.

Fails when an operation is not mapped, is mapped twice, or the map names an
operation the contract does not have, so a contract change cannot reach a
release without a reviewed method name.

    sdkgen.py ts <contract.yaml> <section> <resources.yaml> <out dir> \
        --types-module ./rest.js --root Rest
    sdkgen.py py <contract.yaml> <section> <resources.yaml> <package dir> --root Rest
    sdkgen.py go <contract.yaml> <section> <resources.yaml> <out.go> --fields fields.json --package bma
    sdkgen.py check <contract.yaml> <section> <resources.yaml>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

METHODS = ("get", "post", "put", "patch", "delete")
# Path Item Object fields that are not operations (OpenAPI 3.1 §4.8.9).
PATH_ITEM_FIELDS = ("$ref", "summary", "description", "servers", "parameters")
SCOPE_PATH = {"orgID": "org_id", "projectID": "project_id"}
SCOPE_HEADER = {"x-bma-project-id": "project_id"}
IDEMPOTENCY_HEADER = "Idempotency-Key"
JSON = "application/json"
SSE = "text/event-stream"
BINARY = ("application/octet-stream", "*/*")


class GenError(Exception):
    pass


@dataclass
class Param:
    name: str  # wire name
    key: str  # params field name
    location: str  # path | query | header
    required: bool
    style: str = "form"
    scope: bool = False


@dataclass
class Operation:
    op_id: str
    method: str
    path: str
    params: list[Param]
    body_kind: str | None  # json | binary | multipart | None
    body_required: bool
    body_has_required_fields: bool
    multipart_files: list[str]
    multipart_json: list[str]
    response_kind: str  # json | void | binary | sse
    response_codes: list[int]
    response_refs: list[str | None]
    idempotency: bool
    paginated: bool = False
    unsupported: str | None = None  # why the shape has no resource method
    sse_events: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Method:
    name: str
    op: Operation
    positional: list[Param]


@dataclass
class Resource:
    name: str  # property name, e.g. sessions
    class_name: str
    methods: list[Method]
    children: list["Resource"]


class Contract:
    def __init__(self, document: dict[str, Any], header_names: dict[str, str]):
        self.doc = document
        self.header_names = header_names

    def deref(self, node: Any) -> Any:
        seen = 0
        while isinstance(node, dict) and "$ref" in node:
            target: Any = self.doc
            for part in node["$ref"].removeprefix("#/").split("/"):
                target = target[part]
            node = target
            seen += 1
            if seen > 32:
                raise GenError("$ref cycle")
        return node

    def operations(self) -> dict[str, Operation]:
        out: dict[str, Operation] = {}
        for path, item in self.doc["paths"].items():
            for key in item:
                if key not in METHODS and key not in PATH_ITEM_FIELDS and not key.startswith("x-"):
                    raise GenError(f"{path}: unsupported HTTP method {key} (the SDKs only send {', '.join(METHODS)})")
            for method in METHODS:
                raw = item.get(method)
                if raw is None:
                    continue
                op = self.operation(path, method, item.get("parameters", []) + raw.get("parameters", []), raw)
                if op.op_id in out:
                    raise GenError(f"duplicate operationId {op.op_id}")
                out[op.op_id] = op
        return out

    def required_fields(self, schema: Any) -> bool:
        schema = self.deref(schema)
        if not isinstance(schema, dict):
            return False
        if schema.get("required"):
            return True
        if any(self.required_fields(s) for s in schema.get("allOf", [])):
            return True
        branches = schema.get("oneOf") or schema.get("anyOf")
        if branches:
            return all(self.required_fields(s) for s in branches)
        return False

    def operation(self, path: str, method: str, raw_params: list[Any], raw: dict[str, Any]) -> Operation:
        op_id = raw["operationId"]
        params: list[Param] = []
        idempotency = False
        problems: list[str] = []
        for p in (self.deref(x) for x in raw_params):
            name, loc = p["name"], p["in"]
            if loc == "path":
                scope = name in SCOPE_PATH
                params.append(Param(name, SCOPE_PATH.get(name, name), loc, True, scope=scope))
            elif loc == "query":
                params.append(Param(name, name, loc, bool(p.get("required")), p.get("style", "form")))
            elif loc == "header":
                if name == IDEMPOTENCY_HEADER:
                    idempotency = True
                elif name.lower() in SCOPE_HEADER:
                    params.append(Param(name, SCOPE_HEADER[name.lower()], loc, False, scope=True))
                elif name in self.header_names:
                    params.append(Param(name, self.header_names[name], loc, bool(p.get("required"))))
                else:
                    problems.append(f"header parameter {name} has no name in sdk.resources.yaml header_params")
            else:
                raise GenError(f"{op_id}: unsupported parameter location {loc}")

        body_kind = None
        body_required = False
        body_has_required = False
        files: list[str] = []
        json_fields: list[str] = []
        if "requestBody" in raw:
            rb = self.deref(raw["requestBody"])
            body_required = bool(rb.get("required"))
            content = rb["content"]
            if list(content) == [JSON]:
                body_kind = "json"
                body_has_required = self.required_fields(content[JSON]["schema"])
            elif list(content) == ["multipart/form-data"]:
                body_kind = "multipart"
                media = content["multipart/form-data"]
                schema = self.deref(media["schema"])
                props: dict[str, Any] = dict(schema.get("properties", {}))
                for branch in schema.get("oneOf", []) + schema.get("anyOf", []):
                    props.update(self.deref(branch).get("properties", {}))
                files = sorted(k for k, v in props.items() if self.deref(v).get("format") == "binary")
                json_fields = sorted(
                    k for k, v in (media.get("encoding") or {}).items() if v.get("contentType") == JSON
                )
                body_has_required = self.required_fields(schema)
            elif len(content) == 1 and next(iter(content)) in ("application/octet-stream", "text/plain"):
                body_kind = "binary"
                body_has_required = body_required
            else:
                problems.append(f"unsupported request content {list(content)}")

        codes: list[int] = []
        refs: list[str | None] = []
        kinds: set[str] = set()
        sse_events: list[dict[str, Any]] = []
        for code, resp in raw["responses"].items():
            if not re.fullmatch(r"2\d\d", str(code)):
                continue
            resp = self.deref(resp)
            content = resp.get("content") or {}
            if not content:
                kinds.add("void")
                continue
            if JSON in content:
                kinds.add("json")
                codes.append(int(code))
                ref = content[JSON].get("schema", {}).get("$ref")
                refs.append(ref.split("/")[-1] if ref else None)
            elif SSE in content:
                kinds.add("sse")
                sse_events = self.sse_events(op_id, content[SSE])
            elif any(ct in content for ct in BINARY):
                kinds.add("binary")
            else:
                problems.append(f"unsupported response content {list(content)}")
        if len(kinds) != 1:
            problems.append(f"2xx responses are {sorted(kinds) or 'absent'}")
        unsupported = "; ".join(problems) or None
        kind = kinds.pop() if len(kinds) == 1 else "void"

        self.check_flat_names(op_id, params, body_kind, raw)
        op = Operation(
            op_id, method.upper(), path, params, body_kind, body_required, body_has_required,
            files, json_fields, kind, codes, refs, idempotency, sse_events=sse_events, unsupported=unsupported,
        )
        op.paginated = self.is_cursor_page(op, raw)
        return op

    def body_properties(self, schema: Any, depth: int = 0) -> set[str]:
        """Top-level property names of a body schema, across allOf/oneOf/anyOf branches."""
        schema = self.deref(schema)
        if not isinstance(schema, dict) or depth > 16:
            return set()
        names = set(schema.get("properties") or {})
        for key in ("allOf", "oneOf", "anyOf"):
            for branch in schema.get(key) or []:
                names |= self.body_properties(branch, depth + 1)
        return names

    def check_flat_names(self, op_id: str, params: list[Param], body_kind: str | None, raw: dict[str, Any]) -> None:
        """Methods take one flat params object: scope keys, query, headers and the
        body's top-level fields share a namespace, so a name may appear once."""
        owners: dict[str, str] = {}

        def claim(key: str, owner: str) -> None:
            if key in owners and owners[key] != owner:
                raise GenError(f"{op_id}: flattened params name {key} is both {owners[key]} and {owner}")
            owners[key] = owner

        for p in params:
            if p.scope:
                claim(p.key, "scope")
            elif p.location != "path":
                claim(p.key, p.location)
        if body_kind == "binary":
            claim("body", "binary body")
        elif body_kind in ("json", "multipart"):
            rb = self.deref(raw["requestBody"])
            media = next(iter(rb["content"].values()))
            for name in sorted(self.body_properties(media["schema"])):
                claim(name, "body")

    def is_cursor_page(self, op: Operation, raw: dict[str, Any]) -> bool:
        if op.response_kind != "json" or not any(p.name == "cursor" and p.location == "query" for p in op.params):
            return False
        schema = self.deref(raw["responses"]["200"]["content"][JSON]["schema"])
        props = schema.get("properties", {})
        return "next_cursor" in props and self.deref(props.get("data", {})).get("type") == "array"

    def sse_events(self, op_id: str, media: dict[str, Any]) -> list[dict[str, Any]]:
        item = media.get("x-sse-item-schema")
        if item is None:
            raise GenError(f"{op_id}: text/event-stream response has no x-sse-item-schema")
        events = []
        for branch in item["oneOf"]:
            props = branch["properties"]
            schema_ref = props["data"]["contentSchema"]["$ref"].split("/")[-1]
            events.append({
                "event": props["event"]["const"],
                "durable": "id" in branch.get("required", []),
                "schema": schema_ref,
            })
        return events


def pascal(name: str) -> str:
    return name[0].upper() + name[1:]


def camel_arg(name: str) -> str:
    # agentID -> agentId, terminalSessionID -> terminalSessionId, session_id -> sessionId
    name = re.sub(r"ID$", "Id", name)
    parts = name.split("_")
    return parts[0] + "".join(pascal(p) for p in parts[1:])


def build_tree(section: dict[str, Any], ops: dict[str, Operation]) -> tuple[list[Resource], set[str]]:
    used: dict[str, str] = {}

    def node(name: str, spec: dict[str, Any], prefix: str) -> Resource:
        class_name = prefix + pascal(name)
        methods = []
        for method_name, target in (spec.get("methods") or {}).items():
            if isinstance(target, str):
                op_id, positional_scope = target, []
            else:
                op_id, positional_scope = target["operation"], list(target.get("positional", []))
            if op_id not in ops:
                raise GenError(f"sdk.resources.yaml maps unknown operation {op_id}")
            if op_id in used:
                raise GenError(f"{op_id} is mapped twice ({used[op_id]} and {class_name}.{method_name})")
            used[op_id] = f"{class_name}.{method_name}"
            op = ops[op_id]
            if op.unsupported:
                raise GenError(f"{op_id}: {op.unsupported}; list it under internal or add generator support")
            for name_ in positional_scope:
                if not any(p.name == name_ and p.scope for p in op.params):
                    raise GenError(f"{op_id}: positional {name_} is not a scope path parameter")
            positional = [
                p for p in op.params
                if p.location == "path" and (not p.scope or p.name in positional_scope)
            ]
            methods.append(Method(method_name, op, positional))
        children = [node(k, v, class_name) for k, v in (spec.get("subresources") or {}).items()]
        return Resource(name, class_name, methods, children)

    roots = [node(k, v, "") for k, v in section["resources"].items()]
    internal = set(section.get("internal") or [])
    for op_id in internal:
        if op_id not in ops:
            raise GenError(f"internal lists unknown operation {op_id}")
        if op_id in used:
            raise GenError(f"{op_id} is both internal and mapped to {used[op_id]}")
    missing = sorted(set(ops) - set(used) - internal)
    if missing:
        raise GenError(
            "operations not mapped in sdk.resources.yaml (add a method or list them under internal): "
            + ", ".join(missing)
        )
    return roots, set(used)


# --- TypeScript -------------------------------------------------------------

TS_IDENT = re.compile(r"^[A-Za-z_$][A-Za-z0-9_$]*$")


def ts_prop(name: str) -> str:
    return name if TS_IDENT.match(name) else json.dumps(name)


class TypeScript:
    def __init__(self, contract: Contract, ops: dict[str, Operation], types_module: str, root: str, kind: str):
        self.contract = contract
        self.ops = ops
        self.types_module = types_module
        self.root = root
        self.kind = kind  # rest | facade

    def opref(self, op: Operation) -> str:
        return f'operations["{op.op_id}"]'

    def params_type(self, op: Operation) -> tuple[str, bool]:
        """Returns the params type expression and whether params may be omitted."""
        parts: list[str] = []
        required = False
        scope_keys = sorted({p.key for p in op.params if p.scope})
        if scope_keys:
            parts.append("{ " + " ".join(f"{k}?: string;" for k in scope_keys) + " }")
        if any(p.location == "query" for p in op.params):
            parts.append(f'NonNullable<{self.opref(op)}["parameters"]["query"]>')
            required |= any(p.required for p in op.params if p.location == "query")
        headers = [p for p in op.params if p.location == "header" and not p.scope]
        if headers:
            fields = " ".join(
                f'{p.key}{"" if p.required else "?"}: NonNullable<{self.opref(op)}["parameters"]["header"]>[{json.dumps(p.name)}];'
                for p in headers
            )
            parts.append("{ " + fields + " }")
            required |= any(p.required for p in headers)
        body_ref = f'NonNullable<{self.opref(op)}["requestBody"]>["content"]'
        if op.body_kind == "json":
            body = f'{body_ref}["application/json"]'
            parts.append(body if op.body_required else f"OptionalBody<{body}>")
            required |= op.body_required and op.body_has_required_fields
        elif op.body_kind == "multipart":
            files = " | ".join(json.dumps(f) for f in op.multipart_files) or "never"
            parts.append(f'MultipartBody<{body_ref}["multipart/form-data"], {files}>')
            required |= op.body_required and op.body_has_required_fields
        elif op.body_kind == "binary":
            parts.append("{ body: Uploadable }" if op.body_required else "{ body?: Uploadable }")
            required |= op.body_required
        if not parts:
            return "{}", True
        return " & ".join(parts), not required

    def response_type(self, op: Operation) -> str:
        if op.response_kind == "void":
            return "void"
        if op.response_kind == "binary":
            return "Response"
        if op.response_kind == "sse":
            return "never"
        out = []
        for code, ref in zip(op.response_codes, op.response_refs):
            out.append(f"T.{ref}" if ref else f'{self.opref(op)}["responses"][{code}]["content"]["application/json"]')
        return " | ".join(dict.fromkeys(out))

    def descriptor(self, op: Operation) -> str:
        d: dict[str, Any] = {"id": op.op_id, "method": op.method, "path": op.path}
        if path := [p.name for p in op.params if p.location == "path"]:
            d["pathParams"] = {p.name: p.key for p in op.params if p.location == "path"}
        if query := [p for p in op.params if p.location == "query"]:
            d["query"] = {p.name: p.style for p in query}
        if headers := [p for p in op.params if p.location == "header"]:
            d["headers"] = {p.name: p.key for p in headers}
        if op.body_kind:
            d["body"] = op.body_kind
            if op.body_required:
                d["bodyRequired"] = True
        if op.multipart_json:
            d["multipartJSON"] = op.multipart_json
        d["response"] = op.response_kind
        if op.idempotency:
            d["idempotency"] = True
        return json.dumps(d)

    def method(self, m: Method) -> list[str]:
        op = m.op
        args = [f"{camel_arg(p.name)}: string" for p in m.positional]
        ptype_name = pascal(op.op_id) + "Params"
        _, optional = self.params_type(op)
        args.append(f"params: {ptype_name}" + (" = {}" if optional else ""))
        args.append("options?: RequestOptions")
        path_args = "{ " + ", ".join(f"{p.name}: {camel_arg(p.name)}" for p in m.positional) + " }"
        doc = f"  /** `{op.method} {op.path}` ({op.op_id}) */"
        if op.response_kind == "sse":
            item = pascal(op.op_id) + "Event"
            return [
                doc,
                f"  {m.name}({', '.join(args)}): Stream<{item}> {{",
                f"    return this._client._stream<{item}>(OP.{op.op_id}, {path_args}, params, options);",
                "  }",
            ]
        resp = self.response_type(op)
        if op.paginated:
            return [
                doc,
                f"  {m.name}({', '.join(args)}): PagePromise<{resp}> {{",
                f"    return this._client._page<{resp}>(OP.{op.op_id}, {path_args}, params, options);",
                "  }",
            ]
        return [
            doc,
            f"  {m.name}({', '.join(args)}): Promise<{resp}> {{",
            f"    return this._client._request<{resp}>(OP.{op.op_id}, {path_args}, params, options);",
            "  }",
        ]

    def sse_union(self, op: Operation) -> str:
        members = []
        for e in op.sse_events:
            if e["event"] == "error":
                continue
            if e["durable"]:
                members.append(
                    f'  | {{ event: "{e["event"]}"; id: string; sequence: number; data: T.{e["schema"]} }}'
                )
            else:
                members.append(f'  | {{ event: "{e["event"]}"; data: T.{e["schema"]} }}')
        return "\n".join(members)

    def header(self) -> list[str]:
        return [
            "// Code generated by tools/sdkgen/sdkgen.py from the contract and",
            "// contracts/bma/sdk.resources.yaml; DO NOT EDIT.",
        ]

    def render_operations(self, roots: list[Resource]) -> str:
        """Request descriptors and params/event types (no runtime imports)."""
        out = self.header() + [
            f'import type {{ operations }} from "{self.types_module}";',
            f'import type * as T from "{self.types_module.replace(".js", "-types.js")}";',
            'import type { MultipartBody, OperationDescriptor, OptionalBody, Uploadable } from "../core.js";',
            "",
        ]
        used_ops = sorted((m.op for r in walk(roots) for m in r.methods), key=lambda o: o.op_id)
        out.append("/** Request descriptors, one per mapped contract operation. */")
        out.append("export const OP = {")
        for op in used_ops:
            out.append(f"  {op.op_id}: {self.descriptor(op)},")
        out.append("} as const satisfies Record<string, OperationDescriptor>;")
        for op in used_ops:
            ptype, _ = self.params_type(op)
            out.append("")
            out.append(f"/** Params of `{op.op_id}`: query, header and body fields, flattened. */")
            out.append(f"export type {pascal(op.op_id)}Params = {ptype};")
            if op.response_kind == "sse":
                out.append(f"/** One frame of `{op.op_id}`, discriminated by the SSE event name. */")
                out.append(f"export type {pascal(op.op_id)}Event =\n{self.sse_union(op)};")
        return "\n".join(out) + "\n"

    def render_resources(self, roots: list[Resource], ops_module: str) -> str:
        out = self.header() + [
            f'import type * as T from "{self.types_module.replace(".js", "-types.js")}";',
            f'import type {{ operations }} from "{self.types_module}";',
            'import { ClientCore, type RequestOptions } from "../core.js";',
            'import type { PagePromise } from "../pagination.js";',
            'import type { Stream } from "../streaming.js";',
            'import { APIResource } from "../resource.js";',
            f'import {{ OP }} from "{ops_module}";',
        ]
        param_types = sorted(
            {pascal(m.op.op_id) + "Params" for r in walk(roots) for m in r.methods}
            | {pascal(m.op.op_id) + "Event" for r in walk(roots) for m in r.methods if m.op.response_kind == "sse"}
        )
        out.append(f'import type {{ {", ".join(param_types)} }} from "{ops_module}";')
        for name in sorted({r.class_name for r in walk(roots) if r.class_name in MIXINS}):
            module, base = MIXINS[name]
            out.append(f'import {{ {base} }} from "{module}";')
        out.append("")
        for r in walk(roots):
            base = MIXINS[r.class_name][1] if r.class_name in MIXINS else "APIResource"
            out.append(f"export class {r.class_name} extends {base} {{")
            for c in r.children:
                out.append(f"  readonly {c.name}: {c.class_name} = new {c.class_name}(this._client);")
            if r.children and r.methods:
                out.append("")
            for i, m in enumerate(r.methods):
                if i:
                    out.append("")
                out.extend(self.method(m))
            out.append("}")
            out.append("")
        out.append(f"/** Client with the top-level resources of the {self.kind} API. */")
        out.append(f"export class {self.root}ClientBase extends ClientCore {{")
        for r in roots:
            out.append(f"  readonly {r.name}: {r.class_name} = new {r.class_name}(this);")
        out.append("}")
        return "\n".join(out) + "\n"

    def render_types(self) -> str:
        names = sorted(self.contract.doc.get("components", {}).get("schemas", {}))
        out = [
            "// Code generated by tools/sdkgen/sdkgen.py; DO NOT EDIT.",
            "// A named alias for every contract schema.",
            f'import type {{ components }} from "{self.types_module}";',
            "",
            'type S = components["schemas"];',
        ]
        for n in names:
            if not TS_IDENT.match(n):
                raise GenError(f"schema name {n} is not a TypeScript identifier")
            out.append(f'export type {n} = S["{n}"];')
        return "\n".join(out) + "\n"


# Resource classes that extend a hand-written base adding methods the contract
# cannot describe (verified downloads, the custom tool runner).
MIXINS = {
    "AgentsToolCalls": ("../lib/tool-runner.js", "ToolCallsBase"),
    "AgentsArtifacts": ("../lib/artifacts.js", "ArtifactsBase"),
}


def walk(roots: list[Resource]):
    for r in roots:
        yield from walk(r.children)
        yield r


# Python mixins: same classes as MIXINS, hand-written in bma_sdk.lib.
PY_MIXINS = {
    "AgentsToolCalls": ("...lib.tools", "ToolCallsBase"),
    "AgentsArtifacts": ("...lib.artifacts", "ArtifactsBase"),
}


def write_python(contract: Contract, roots: list[Resource], section: str, root: str, out: Path, count: int) -> int:
    sys.path.insert(0, str(Path(__file__).parent))
    from pygen import PyGenError, PythonResources

    gen = PythonResources(contract, roots, section, section, root, PY_MIXINS)
    try:
        resources = gen.render_resources()  # first: registers the types it uses
        files = {
            "operations.py": gen.render_operations(),
            "resources.py": resources,
            "models.py": gen.render_models(),
            "params.py": gen.render_params(),
            "__init__.py": "# Code generated by tools/sdkgen/sdkgen.py; DO NOT EDIT.\n",
        }
    except PyGenError as e:
        print(f"sdkgen: {e}", file=sys.stderr)
        return 1
    out.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (out / name).write_text(text)
    print(f"wrote {out}/{{models,params,operations,resources}}.py ({count} methods)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("lang", choices=["ts", "py", "go", "check"])
    ap.add_argument("contract")
    ap.add_argument("section")
    ap.add_argument("resources")
    ap.add_argument("out", nargs="?", help="output directory")
    ap.add_argument("--types-module", default="./rest.js")
    ap.add_argument("--root", default="Rest")
    ap.add_argument("--fields", help="go: gofields JSON of the oapi-codegen models")
    ap.add_argument("--package", default="bma")
    a = ap.parse_args()

    config = yaml.safe_load(Path(a.resources).read_text())
    contract = Contract(yaml.safe_load(Path(a.contract).read_text()), config.get("header_params") or {})
    try:
        ops = contract.operations()
        roots, used = build_tree(config[a.section], ops)
    except GenError as e:
        print(f"sdkgen: {e}", file=sys.stderr)
        return 1
    if a.lang == "check":
        print(f"sdkgen: {len(used)} mapped + {len(ops) - len(used)} internal = {len(ops)} operations")
        return 0
    if a.lang == "go":
        sys.path.insert(0, str(Path(__file__).parent))
        from gogen import Go, GoGenError

        try:
            text = Go(contract, roots, json.loads(Path(a.fields).read_text()), a.package, ops).render()
        except GoGenError as e:
            print(f"sdkgen: {e}", file=sys.stderr)
            return 1
        Path(a.out).write_text(text)
        print(f"wrote {a.out} ({len(used)} methods)")
        return 0
    if a.lang == "py":
        return write_python(contract, roots, a.section, a.root, Path(a.out), len(used))
    ts = TypeScript(contract, ops, a.types_module, a.root, a.section)
    out = Path(a.out)
    base = a.types_module.removeprefix("./").removesuffix(".js")
    try:
        (out / f"{base}-operations.ts").write_text(ts.render_operations(roots))
        (out / f"{base}-resources.ts").write_text(ts.render_resources(roots, f"./{base}-operations.js"))
        (out / f"{base}-types.ts").write_text(ts.render_types())
    except GenError as e:
        print(f"sdkgen: {e}", file=sys.stderr)
        return 1
    print(f"wrote {out}/{base}-{{operations,resources,types}}.ts ({len(used)} methods)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
