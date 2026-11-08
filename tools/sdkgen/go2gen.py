#!/usr/bin/env python3
"""Generate the bma-sdk 2.0 extension services (v2/generated_resources.go).

Input: contracts/bma/v2/extensions.openapi.yaml, the resource map
contracts/bma/v2/sdk.resources.yaml, and the Go models oapi-codegen wrote
(v2/generated_models.go; schema types must exist there). Every operation must
be mapped to a method or to `official`, otherwise generation fails.

Methods follow anthropic-sdk-go: New/Get/Update/List/ListAutoPaging/Delete
and path actions in CamelCase; path parameters are positional strings, the
request body or the query is one <Stem><Method>Params value. Requests go
through the official client (request.go: execute), so options, retries and
errors are the official ones.

  python3 tools/sdkgen/go2gen.py <contract> <resources.yaml> <models.go> <out.go>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

METHODS = ("get", "post", "put", "patch", "delete")
HTTP = {"get": "MethodGet", "post": "MethodPost", "put": "MethodPut", "patch": "MethodPatch", "delete": "MethodDelete"}
INITIALISMS = {"id": "ID", "url": "URL", "api": "API", "ids": "IDs"}


def camel(snake: str, lower_first: bool = False) -> str:
    parts = [INITIALISMS.get(p, p[:1].upper() + p[1:]) for p in snake.split("_") if p]
    out = "".join(parts)
    if lower_first:
        first = parts[0]
        out = (first.lower() if first.isupper() else first[:1].lower() + first[1:]) + "".join(parts[1:])
    return out


def ref_name(schema: dict) -> str | None:
    ref = schema.get("$ref")
    return ref.rsplit("/", 1)[-1] if ref else None


def go_scalar(schema: dict) -> str:
    t = schema.get("type")
    if isinstance(t, list):
        t = next(x for x in t if x != "null")
    return {"integer": "int64", "boolean": "bool", "string": "string"}.get(t) or sys.exit(f"unsupported query type {schema}")


class Gen:
    def __init__(self, contract: dict, resources: dict, models: str):
        self.doc = contract
        self.res = resources
        self.types = set(re.findall(r"^type (\w+) ", models, re.M))
        self.params = contract["components"].get("parameters", {})
        self.schemas = contract["components"]["schemas"]
        self.skip_query = set(resources.get("skip_query", []))

    def go_type(self, name: str) -> str:
        if name not in self.types:
            sys.exit(f"schema {name} has no Go type in the generated models")
        return name

    def param(self, p: dict) -> dict:
        return self.params[ref_name(p)] if "$ref" in p else p

    def run(self) -> str:
        services: dict[str, str] = self.res["services"]
        mapping: dict[str, str] = self.res["operations"]
        methods: dict[str, list[str]] = {s: [] for s in services}
        extra_types: list[str] = []
        seen = set()
        for path, item in self.doc["paths"].items():
            for verb in METHODS:
                op = item.get(verb)
                if not isinstance(op, dict):
                    continue
                op_id = op["operationId"]
                seen.add(op_id)
                target = mapping.get(op_id) or sys.exit(f"operation {op_id} is not in sdk.resources.yaml")
                if target == "official":
                    continue
                service, method = target.rsplit(".", 1)
                if service not in services:
                    sys.exit(f"{op_id}: unknown service {service}")
                code, types = self.method(services[service], method, verb, path, op)
                methods[service].append(code)
                extra_types.extend(types)
        stale = set(mapping) - seen
        if stale:
            sys.exit(f"sdk.resources.yaml maps operations the contract does not have: {sorted(stale)}")
        return self.render(services, methods, extra_types)

    def method(self, stem: str, method: str, verb: str, path: str, op: dict):
        svc = stem + "Service"
        path_params = re.findall(r"{(\w+)}", path)
        go_path = "v1" + re.sub(r"{(\w+)}", "%s", path)
        args = ", ".join(f"{camel(p, True)} string" for p in path_params)
        args = (args + ", ") if args else ""
        checks = "".join(
            f'\tif {camel(p, True)} == "" {{\n\t\terr = errors.New("missing required {p} parameter")\n\t\treturn\n\t}}\n'
            for p in path_params
        )
        fmt_args = "".join(f", url.PathEscape({camel(p, True)})" for p in path_params)
        path_expr = f'fmt.Sprintf("{go_path}"{fmt_args})' if path_params else f'"{go_path}"'

        params = [self.param(p) for p in op.get("parameters", [])]
        queries = [p for p in params if p["in"] == "query" and p["name"] not in self.skip_query]
        idem = any(p["in"] == "header" and p["name"] == "Idempotency-Key" for p in params)
        body = op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema")
        if body and queries:
            sys.exit(f"{op['operationId']}: body and query parameters together are not supported")

        resp = self.response(op)
        params_type = f"{stem}{method}Params"
        types: list[str] = []
        param_arg = ""
        param_val = "nil"
        if body:
            name = ref_name(body) or sys.exit(f"{op['operationId']}: inline request body")
            types.append(
                f"// {params_type} is the request body of {stem}Service.{method}.\ntype {params_type} = {self.go_type(name)}\n"
            )
            param_arg, param_val = f"params {params_type}, ", "params"
        elif queries:
            fields, sets = [], []
            for q in queries:
                field = camel(q["name"])
                desc = (q.get("description") or q.get("schema", {}).get("description") or "").strip().replace("\n", " ")
                if desc:
                    fields.append(f"\t// {field} {desc}")
                fields.append(f'\t{field} *{go_scalar(q["schema"])} `query:"{q["name"]}"`')
                fmt = {"int64": "strconv.FormatInt(*r.{f}, 10)", "bool": "strconv.FormatBool(*r.{f})", "string": "*r.{f}"}[
                    go_scalar(q["schema"])
                ].format(f=field)
                sets.append(f'\tif r.{field} != nil {{\n\t\tv.Set("{q["name"]}", {fmt})\n\t}}')
            types.append(
                f"// {params_type} is the query of {stem}Service.{method}.\ntype {params_type} struct {{\n"
                + "\n".join(fields)
                + f"\n}}\n\n// URLQuery serializes {params_type} as URL query parameters.\n"
                + f"func (r {params_type}) URLQuery() (url.Values, error) {{\n\tv := url.Values{{}}\n"
                + "\n".join(sets)
                + "\n\treturn v, nil\n}\n"
            )
            param_arg, param_val = f"params {params_type}, ", "params"

        summary = op.get("summary", "").strip().rstrip(".")
        doc = f"// {method} sends {verb.upper()} /v1{path}: {summary}."
        if op.get("description"):
            doc += " " + " ".join(op["description"].split())
        doc += "\n"
        pre = "[]option.RequestOption{autoIdempotencyKey()}, " if idem else ""

        if resp[0] == "list":
            item = resp[1]
            code = (
                f"{doc}func (r *{svc}) {method}(ctx context.Context, {args}{param_arg}opts ...option.RequestOption) (res *Page[{item}], err error) {{\n"
                f"{checks}\topts = slices.Concat(r.Options, opts)\n"
                + (f"\tq, err := {param_val}.URLQuery()\n\tif err != nil {{\n\t\treturn\n\t}}\n" if queries else "\tq := url.Values{}\n")
                + f"\treturn listPage[{item}](ctx, {path_expr}, query(q), \"\", opts)\n}}\n\n"
                f"// {method}AutoPaging iterates every item of {method} across pages.\n"
                f"func (r *{svc}) {method}AutoPaging(ctx context.Context, {args}{param_arg}opts ...option.RequestOption) *PageAutoPager[{item}] {{\n"
                f"\treturn NewPageAutoPager(r.{method}(ctx, "
                + "".join(f"{camel(p, True)}, " for p in path_params)
                + ("params, " if param_arg else "")
                + "opts...))\n}\n"
            )
        else:
            code = (
                f"{doc}func (r *{svc}) {method}(ctx context.Context, {args}{param_arg}opts ...option.RequestOption) (res *{resp[1]}, err error) {{\n"
                f"{checks}\topts = slices.Concat(r.Options, {pre}opts)\n"
                f"\terr = execute(ctx, http.{HTTP[verb]}, {path_expr}, {param_val}, &res, opts...)\n\treturn\n}}\n"
            )
        return code, types

    def response(self, op: dict):
        ok = [c for c in op["responses"] if str(c).startswith("2")]
        content = op["responses"][ok[0]].get("content", {})
        schema = content.get("application/json", {}).get("schema") or sys.exit(f"{op['operationId']}: no JSON response")
        name = ref_name(schema) or sys.exit(f"{op['operationId']}: inline response")
        props = self.schemas[name].get("properties", {})
        if set(props) == {"data", "next_page"}:
            return ("list", self.go_type(ref_name(props["data"]["items"])))
        return ("object", self.go_type(name))

    def render(self, services: dict[str, str], methods: dict[str, list[str]], extra_types: list[str]) -> str:
        out = [
            "// Code generated by tools/sdkgen/go2gen.py from contracts/bma/v2/extensions.openapi.yaml; DO NOT EDIT.\n",
            "package bmasdk\n",
            'import (\n\t"context"\n\t"errors"\n\t"fmt"\n\t"net/http"\n\t"net/url"\n\t"slices"\n\t"strconv"\n\n'
            '\t"github.com/anthropics/anthropic-sdk-go/v2/option"\n)\n',
            "var (\n\t_ = errors.New\n\t_ = fmt.Sprintf\n\t_ = strconv.Itoa\n\t_ = http.MethodGet\n)\n",
        ]
        children: dict[str, list[str]] = {}
        for path in services:
            if "." in path:
                parent, leaf = path.rsplit(".", 1)
                children.setdefault(parent, []).append(path)
        top = [p for p in services if "." not in p]
        out.append("// extensionServices are the BMA extension resources of client.Beta.\ntype extensionServices struct {")
        for p in top:
            out.append(f"\t{p} {services[p]}Service")
        out.append("}\n")
        out.append("func newExtensionServices(opts []option.RequestOption) extensionServices {\n\treturn extensionServices{")
        for p in top:
            out.append(f"\t\t{p}: new{services[p]}Service(opts),")
        out.append("\t}\n}\n")
        for path, stem in services.items():
            leaf = path.rsplit(".", 1)[-1]
            out.append(f"// {stem}Service is client.Beta.{path}.\ntype {stem}Service struct {{\n\tOptions []option.RequestOption")
            for child in children.get(path, []):
                out.append(f"\t{child.rsplit('.', 1)[-1]} {services[child]}Service")
            out.append("}\n")
            out.append(f"func new{stem}Service(opts []option.RequestOption) {stem}Service {{\n\treturn {stem}Service{{\n\t\tOptions: opts,")
            for child in children.get(path, []):
                out.append(f"\t\t{child.rsplit('.', 1)[-1]}: new{services[child]}Service(opts),")
            out.append("\t}\n}\n")
            out.extend(methods[path])
            del leaf
        out.extend(extra_types)
        return "\n".join(out) + "\n"


def main() -> int:
    if len(sys.argv) != 5:
        print(__doc__, file=sys.stderr)
        return 2
    contract, resources, models, target = map(Path, sys.argv[1:])
    gen = Gen(yaml.safe_load(contract.read_text()), yaml.safe_load(resources.read_text()), models.read_text())
    target.write_text(gen.run())
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
