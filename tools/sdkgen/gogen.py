"""Go template of tools/sdkgen/sdkgen.py (ADR 0012).

Builds services on top of the oapi-codegen models of one package: one
<Path>Service per resource, methods New/Get/List/Update/Delete/... taking
path IDs positionally and a <Path><Method>Params struct whose fields are the
operation's query, header and body fields (copied from the oapi-codegen
<Op>Params and request body structs, read by tools/sdkgen/gofields), plus
List...AutoPaging for cursor pages, typed SSE events with AsAny(), and
AsAny() on every discriminated union.
"""
from __future__ import annotations

import re
from typing import Any

INITIALISMS = {"api": "API", "mcp": "MCP", "url": "URL", "id": "ID", "ids": "IDs", "byo": "BYO", "sse": "SSE"}
VERBS = {"create": "New", "retrieve": "Get"}


class GoGenError(Exception):
    pass


def words(name: str) -> list[str]:
    out: list[str] = []
    for part in re.split(r"[_\-]+", name):
        out += re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z0-9]+", part)
    return out


def go_name(name: str) -> str:
    return "".join(INITIALISMS.get(w.lower(), w[:1].upper() + w[1:]) for w in words(name))


def singular(name: str) -> str:
    ws = words(name)
    last = ws[-1]
    if last.endswith("ies"):
        last = last[:-3] + "y"
    elif last.endswith("s") and not last.endswith("ss"):
        last = last[:-1]
    return go_name("_".join(ws[:-1] + [last]))


def arg_name(name: str) -> str:
    n = go_name(name)
    return n[:1].lower() + n[1:] if not n.startswith("ID") else "id" + n[2:]


def method_name(name: str) -> str:
    return VERBS.get(name, go_name(name))


class Go:
    def __init__(self, contract: Any, roots: list[Any], fields: dict[str, Any], package: str, ops_all: dict[str, Any]):
        self.contract = contract
        self.roots = roots
        self.fields = fields
        self.package = package
        self.names: set[str] = set()
        self.events: dict[str, list[tuple[str, str]]] = {}
        self.imports: set[str] = {"context", "github.com/beeos-ai/bma-sdk/internal/apicore", "github.com/beeos-ai/bma-sdk/option"}

    # -- helpers ---------------------------------------------------------------

    def claim(self, name: str) -> str:
        if name in self.fields or name in self.names:
            raise GoGenError(f"generated name {name} collides with another type")
        self.names.add(name)
        return name

    def struct(self, name: str) -> list[dict[str, Any]]:
        t = self.fields.get(name)
        while t and t["kind"] != "struct" and re.fullmatch(r"\w+", t.get("target") or ""):
            name = t["target"]
            t = self.fields.get(name)
        if not t or t["kind"] != "struct":
            raise GoGenError(f"oapi-codegen type {name} is not a struct")
        return t["fields"]

    def resolve(self, name: str) -> str:
        """The body type to construct: aliases resolved, defined types kept."""
        t = self.fields.get(name)
        while t and t["kind"] == "alias":
            name = t["target"]
            t = self.fields.get(name)
        return name

    def raw(self, op: Any) -> dict[str, Any]:
        return self.contract.doc["paths"][op.path][op.method.lower()]

    def walk(self):
        def rec(rs, prefix):
            for r in rs:
                path = prefix + [r.name]
                yield r, path
                yield from rec(r.children, path)
        return list(rec(self.roots, []))

    # -- per operation -------------------------------------------------------------

    def oapi_params(self, op: Any) -> list[dict[str, Any]]:
        name = op.op_id[:1].upper() + op.op_id[1:] + "Params"
        return self.struct(name) if name in self.fields else []

    def param_fields(self, op: Any) -> tuple[list[tuple[str, str]], list[str]]:
        """(Go struct fields, statements that apply them to request r)."""
        fields: list[tuple[str, str]] = []
        stmts: list[str] = []
        oapi = {f.get("form") or f.get("json"): f for f in self.oapi_params(op)}
        resume = next((p for p in op.params if p.location == "header" and p.name.lower() == "last-event-id"), None)
        for p in op.params:
            if p.location == "path" or p.scope:
                continue
            f = oapi.get(p.name)
            if f is None:
                raise GoGenError(f"{op.op_id}: no oapi-codegen field for {p.location} parameter {p.name}")
            fields.append((f["name"], f["type"]))
            if p.location == "query":
                stmt = f'r.Query("{p.name}", "{p.style}", params.{f["name"]})'
                if resume is not None and p.name == "after_sequence":
                    stmt = "if resume == \"\" {\n\t\t\t" + stmt + "\n\t\t}"
            else:
                stmt = f'r.Header("{p.name}", params.{f["name"]})'
                if p is resume:
                    stmt = (f'if resume == "" {{\n\t\t\t{stmt}\n\t\t}} else {{\n\t\t\t'
                            f'r.Header("{p.name}", resume)\n\t\t}}')
            stmts.append(stmt)
        if op.body_kind == "binary":
            self.imports.add("io")
            fields.append(("Body", "io.Reader"))
            stmts.append("r.Binary(params.Body)")
        elif op.body_kind in ("json", "multipart"):
            suffix = "JSONRequestBody" if op.body_kind == "json" else "MultipartRequestBody"
            body_type = self.resolve(op.op_id[:1].upper() + op.op_id[1:] + suffix)
            body = [f for f in self.struct(body_type) if f["name"][:1].isupper()]
            if op.body_kind == "json":
                for f in body:
                    fields.append((f["name"], f["type"]))
                inits = ", ".join(f'{f["name"]}: params.{f["name"]}' for f in body)
                stmts.append(f"r.JSON({body_type}{{{inits}}})")
            else:
                self.imports.add("io")
                for f in body:
                    wire = f["json"]
                    if f["type"].endswith("openapi_types.File"):
                        fields.append((f["name"], "io.Reader"))
                        stmts.append(f'r.MultipartFile("{wire}", params.{f["name"]})')
                    else:
                        fields.append((f["name"], f["type"]))
                        as_json = "true" if wire in op.multipart_json else "false"
                        stmts.append(f'r.MultipartField("{wire}", params.{f["name"]}, {as_json})')
        for _, t in fields:
            if "openapi_types." in t:
                self.imports.add('openapi_types "github.com/oapi-codegen/runtime/types"')
            if "time." in t:
                self.imports.add("time")
            if "json." in t:
                self.imports.add("encoding/json")
        names = [n for n, _ in fields]
        dup = {n for n in names if names.count(n) > 1}
        if dup:
            raise GoGenError(f"{op.op_id}: params fields {sorted(dup)} appear twice")
        return fields, stmts

    def response(self, op: Any) -> str:
        refs = set(op.response_refs)
        if None in refs or len(refs) != 1:
            raise GoGenError(f"{op.op_id}: JSON responses {sorted(map(str, refs))} need one named schema")
        return refs.pop()

    def page_cursor(self, op: Any) -> list[str]:
        """Statements choosing the cursor (param, field): the pair whose
        parameter the caller set, else the default direction."""
        (p0, f0), *others = op.page
        lines = [f'\tparam, field := "{p0}", "{f0}"']
        oapi = {f.get("form") or f.get("json"): f for f in self.oapi_params(op)}
        for p, f in others:
            go_field = oapi[p]["name"]
            if not oapi[p]["type"].startswith("*"):
                raise GoGenError(f"{op.op_id}: cursor parameter {p} is not optional")
            lines += [f"\tif params.{go_field} != nil {{", f'\t\tparam, field = "{p}", "{f}"', "\t}"]
        return lines

    def page_item(self, op: Any) -> str:
        data = next(f for f in self.struct(self.response(op)) if f["json"] == "data")
        if not data["type"].startswith("[]"):
            raise GoGenError(f"{op.op_id}: data is {data['type']}")
        return data["type"][2:]

    def descriptor(self, op: Any) -> str:
        scope = {p.name: ("org" if p.key == "org_id" else "project") for p in op.params if p.scope and p.location == "path"}
        parts = [f'ID: "{op.op_id}"', f'Method: "{op.method}"', f'Path: "{op.path}"']
        return parts, scope

    def method(self, svc: str, m: Any, path_name: str) -> tuple[list[str], list[str]]:
        """Returns (op descriptor lines, method lines)."""
        op = m.op
        name = method_name(m.name)
        positional = [p for p in m.positional]
        scope = {p.name: ("org" if p.key == "org_id" else "project") for p in op.params
                 if p.scope and p.location == "path" and p not in positional}
        header_scope = next((p.name for p in op.params if p.scope and p.location == "header"), "")
        opvar = "op" + op.op_id[:1].upper() + op.op_id[1:]
        desc = [f"var {opvar} = apicore.Op{{", f'\tID: "{op.op_id}", Method: "{op.method}", Path: "{op.path}",']
        if scope:
            desc.append("\tScope: map[string]string{" + ", ".join(f'"{k}": "{v}"' for k, v in sorted(scope.items())) + "},")
        if header_scope:
            desc.append(f'\tScopeHeader: "{header_scope}",')
        if op.idempotency:
            desc.append("\tIdempotency: true,")
        desc.append("}")

        fields, stmts = self.param_fields(op)
        args = ["ctx context.Context"] + [f"{arg_name(p.name)} string" for p in positional]
        ptype = ""
        if fields:
            ptype = self.claim(f"{path_name}{name}Params")
            args.append(f"params {ptype}")
        args.append("opts ...option.RequestOption")
        build = [f"r := s.core.NewRequest(&{opvar}, opts)"]
        build += [f'r.Path("{p.name}", {arg_name(p.name)})' for p in positional]
        build += stmts
        doc = f"// {name} calls {op.op_id}: {op.method} {op.path}."
        lines: list[str] = []
        if ptype:
            lines.append(f"// {ptype} are the query, header and body fields of {op.op_id}.")
            lines.append(f"type {ptype} struct {{")
            lines += [f"\t{n} {t}" for n, t in fields]
            lines += ["}", ""]
        sig = ", ".join(args)
        call_args = ", ".join(["ctx"] + [arg_name(p.name) for p in positional] + (["params"] if ptype else []) + ["opts..."])

        if op.response_kind == "sse":
            ev = self.event_type(op)
            builder = f"{name[:1].lower()}{name[1:]}Request"
            lines += [doc, f"func (s *{svc}) {name}({sig}) *Stream[{ev}] {{",
                      f"\treturn apicore.OpenStream(ctx, s.{builder}({', '.join([arg_name(p.name) for p in positional] + (['params'] if ptype else []) + ['opts'])}), decode{ev}, nil, apicore.UseMaxRetries)",
                      "}", ""]
            lines += [f"func (s *{svc}) {builder}({', '.join(args[1:-1] + ['opts []option.RequestOption'])}) func(resume string) *apicore.Request {{",
                      "\treturn func(resume string) *apicore.Request {"]
            lines += ["\t\t" + b for b in build] + ["\t\treturn r", "\t}", "}", ""]
            return desc, lines
        if op.paginated:
            item = self.page_item(op)
            builder = f"{name[:1].lower()}{name[1:]}Request"
            builder_args = ", ".join([arg_name(p.name) for p in positional] + (["params"] if ptype else []) + ["opts"])
            cursor = self.page_cursor(op)
            lines += [doc, f"func (s *{svc}) {name}({sig}) (*CursorPage[{item}], error) {{"] + cursor + [
                      f"\treturn apicore.FetchPage[{item}](ctx, s.{builder}({builder_args}), param, field, \"\")", "}", "",
                      f"// {name}AutoPaging iterates every item of {op.op_id} across pages.",
                      f"func (s *{svc}) {name}AutoPaging({sig}) *CursorPageAutoPager[{item}] {{"] + cursor + [
                      f"\treturn apicore.NewAutoPager[{item}](ctx, s.{builder}({builder_args}), param, field)", "}", "",
                      f"func (s *{svc}) {builder}({', '.join(args[1:-1] + ['opts []option.RequestOption'])}) func() *apicore.Request {{",
                      "\treturn func() *apicore.Request {"]
            lines += ["\t\t" + b for b in build] + ["\t\treturn r", "\t}", "}", ""]
            return desc, lines
        body = ["\t" + b.replace("\n\t\t", "\n\t") for b in build]
        if op.response_kind == "void":
            lines += [doc, f"func (s *{svc}) {name}({sig}) error {{"] + body + ["\treturn apicore.DoVoid(ctx, r)", "}", ""]
        elif op.response_kind == "binary":
            self.imports.add("net/http")
            lines += [doc, "// The caller closes the response body.", f"func (s *{svc}) {name}({sig}) (*http.Response, error) {{"] + body + ["\treturn apicore.DoRaw(ctx, r)", "}", ""]
        elif len(set(op.response_refs)) > 1:
            # One field per documented status, e.g. a replayed create (200)
            # and a new one (201).
            self.imports |= {"encoding/json", "fmt"}
            resp = self.claim(f"{path_name}{name}Response")
            lines += [f"// {resp} holds the body of whichever success status {op.op_id} returned.", f"type {resp} struct {{"]
            lines += [f"\t{ref} *{ref} // {code}" for code, ref in zip(op.response_codes, op.response_refs)]
            lines += ["}", "", doc, f"func (s *{svc}) {name}({sig}) (*{resp}, error) {{"] + body
            lines += ["\tstatus, raw, err := apicore.DoBytes(ctx, r)", "\tif err != nil {", "\t\treturn nil, err", "\t}",
                      f"\tout := &{resp}{{}}", "\tswitch status {"]
            for code, ref in zip(op.response_codes, op.response_refs):
                lines += [f"\tcase {code}:", f"\t\tout.{ref} = new({ref})", f"\t\terr = json.Unmarshal(raw, out.{ref})"]
            lines += ["\tdefault:", f'\t\terr = fmt.Errorf("bma: {op.op_id}: undocumented status %d", status)', "\t}",
                      "\tif err != nil {", "\t\treturn nil, err", "\t}", "\treturn out, nil", "}", ""]
        else:
            resp = self.response(op)
            lines += [doc, f"func (s *{svc}) {name}({sig}) (*{resp}, error) {{"] + body + [f"\treturn apicore.Do[{resp}](ctx, r)", "}", ""]
        _ = call_args
        return desc, lines

    def event_type(self, op: Any) -> str:
        name = op.op_id[:1].upper() + op.op_id[1:] + "Event"
        if name not in self.events:
            self.claim(name)
            self.events[name] = [(e["event"], e["schema"]) for e in op.sse_events if e["event"] != "error"]
        return name

    def render_events(self) -> list[str]:
        out: list[str] = []
        if self.events:
            self.imports |= {"encoding/json", "fmt"}
        for name, events in self.events.items():
            out += [
                f"// {name} is one server-sent event frame. Event is the SSE event name;",
                "// durable frames also carry ID and Sequence. AsAny returns the decoded",
                "// payload: " + ", ".join(f"{s} ({e})" for e, s in events) + ".",
                f"type {name} struct {{",
                "\tEvent    string",
                "\tID       string",
                "\tSequence int64",
                "\tData     json.RawMessage",
                "\tvalue    any",
                "}",
                "",
                "// AsAny returns the payload as its contract type; switch on it.",
                f"func (e {name}) AsAny() any {{ return e.value }}",
                "",
                f"func decode{name}(event, id string, sequence int64, data []byte) ({name}, bool, error) {{",
                f"\tev := {name}{{Event: event, ID: id, Sequence: sequence, Data: data}}",
                "\tswitch event {",
            ]
            for event, schema in events:
                out += [
                    f'\tcase "{event}":',
                    f"\t\tvar v {schema}",
                    "\t\tif err := json.Unmarshal(data, &v); err != nil {",
                    f'\t\t\treturn ev, false, fmt.Errorf("bma: decode {event} frame: %w", err)',
                    "\t\t}",
                    "\t\tev.value = v",
                ]
            out += ["\tdefault:", "\t\treturn ev, false, nil // an event kind newer than this SDK", "\t}", "\treturn ev, true, nil", "}", ""]
        return out

    def render_unions(self) -> list[str]:
        out: list[str] = []
        for name in sorted(self.fields):
            if "ValueByDiscriminator" in (self.fields[name].get("methods") or []):
                out += [
                    f"// AsAny returns the member of {name} named by its discriminator, or",
                    "// nil for a value this SDK does not know; switch on its type.",
                    f"func (t {name}) AsAny() any {{",
                    "\tv, err := t.ValueByDiscriminator()",
                    "\tif err != nil {",
                    "\t\treturn nil",
                    "\t}",
                    "\treturn v",
                    "}",
                    "",
                ]
        return out

    def render(self) -> str:
        services: list[str] = []
        descriptors: list[str] = []
        for r, path in self.walk():
            path_name = "".join(singular(p) for p in path)
            svc = self.claim(path_name + "Service")
            services += [f"// {svc} groups the {'.'.join(path)} methods.", f"type {svc} struct {{", "\tcore *apicore.Client"]
            for c in r.children:
                services.append(f"\t{go_name(c.name)} *{path_name}{singular(c.name)}Service")
            services += ["}", "", f"func new{svc}(core *apicore.Client) *{svc} {{", f"\treturn &{svc}{{core: core"
                         + "".join(f", {go_name(c.name)}: new{path_name}{singular(c.name)}Service(core)" for c in r.children) + "}", "}", ""]
            for m in r.methods:
                desc, lines = self.method(svc, m, path_name)
                descriptors += desc + [""]
                services += lines
        root = ["// resources are the top-level services of the API.", "type resources struct {"]
        root += [f"\t{go_name(r.name)} *{singular(r.name)}Service" for r in self.roots]
        root += ["}", "", "func newResources(core *apicore.Client) resources {", "\treturn resources{"]
        root += [f"\t\t{go_name(r.name)}: new{singular(r.name)}Service(core)," for r in self.roots]
        root += ["\t}", "}", ""]
        tail = self.render_events() + self.render_unions()
        head = ["// Code generated by tools/sdkgen/sdkgen.py from the contract and", "// contracts/bma/sdk.resources.yaml; DO NOT EDIT.", "",
                f"package {self.package}", "", "import ("]
        head += [f"\t{i}" if " " in i else f'\t"{i}"' for i in sorted(self.imports)] + [")", ""]
        return "\n".join(head + root + descriptors + services + tail) + "\n"
