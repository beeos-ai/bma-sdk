#!/usr/bin/env python3
"""Generate the bma-sdk 2.0 TypeScript extension services.

Input: contracts/bma/v2/extensions.openapi.yaml and the resource map
contracts/bma/v2/sdk.resources.yaml (see v2model.py). The schema types come
from openapi-typescript (typescript/src/generated/extensions.ts).

The services subclass the official APIResource and send every request through
the official client (`this._client.get/post/getAPIList`), so the base URL,
credentials, headers, retries, timeouts, middleware and errors are the
official ones. Methods follow @anthropic-ai/sdk: create / retrieve / update /
list / delete and path actions in camelCase; path parameters are positional,
the request body or the query is one params object.

    python3 tools/sdkgen/ts2gen.py <contract> <resources.yaml> <out dir>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from v2model import Model, Op, Query, Service, camel_case, pascal_case


def ts_type(model: Model, schema: dict) -> str:
    if "$ref" in schema:
        return f"S['{schema['$ref'].rsplit('/', 1)[-1]}']"
    if "enum" in schema:
        return " | ".join(repr(v).replace("'", '"') if isinstance(v, str) else str(v) for v in schema["enum"])
    t = schema.get("type")
    if isinstance(t, list):
        t = next(x for x in t if x != "null")
    return {"integer": "number", "number": "number", "boolean": "boolean", "string": "string"}.get(t) or sys.exit(
        f"unsupported query type {schema}"
    )


def class_name(service: Service) -> str:
    return service.stem + "s"


def prop_name(service: Service) -> str:
    leaf = service.path.rsplit(".", 1)[-1]
    return leaf[:1].lower() + leaf[1:]


def arg_name(param: str) -> str:
    return camel_case(param).removesuffix("Id") + "ID" if param.endswith("_id") else camel_case(param)


def route_of(op: Op) -> str:
    base = "/v1" + op.path
    if not op.path_params:
        return f"'{base}'"
    return "path`" + re.sub(r"{(\w+)}", lambda m: "${" + arg_name(m[1]) + "}", base) + "`"


def doc(op: Op, indent: str = "  ") -> str:
    text = f"{op.summary}." if op.summary else ""
    if op.description:
        text += " " + op.description
    text = text.replace("*/", "*\\/")
    return f"{indent}/**\n{indent} * {text.strip()}\n{indent} */\n"


class Gen:
    def __init__(self, model: Model):
        self.m = model
        self.types: dict[str, str] = {}  # exported alias -> expression
        self.params: list[str] = []

    def alias(self, schema: str) -> str:
        self.types.setdefault(schema, f"S['{schema}']")
        return schema

    def method(self, svc: Service, op: Op) -> str:
        m = self.m
        name = m.method_name(op, "camel")
        stem = svc.stem
        params_type = f"{stem}{pascal_case(name)}Params"
        args = [f"{arg_name(p)}: string" for p in op.path_params]
        call_arg = ""  # "body: params" or "query: params"
        if op.body:
            self.params.append(f"export type {params_type} = {self.alias(op.body)};\n")
            args.append(f"params: {params_type}" + ("" if op.body_required else " = {}"))
            call_arg = "body: params"
        elif op.queries:
            fields = []
            for q in op.queries:
                if q.description:
                    description = q.description.replace("*/", "*\\/")
                    fields.append(f"  /** {description} */")
                fields.append(f"  {q.name}{'' if q.required else '?'}: {ts_type(m, q.schema)};")
            self.params.append(f"export interface {params_type} {{\n" + "\n".join(fields) + "\n}\n")
            args.append(f"params: {params_type} | null | undefined = {{}}")
            call_arg = "query: params"
        args.append("options?: RequestOptions")
        route = route_of(op)
        headers = "headers: mergeHeaders([{ 'Idempotency-Key': newIdempotencyKey() }, options?.headers])"
        init = ", ".join(x for x in (call_arg, "...options", headers if op.idempotent else "") if x)
        if op.paged:
            item = self.alias(op.response)
            ret = f"PagePromise<{stem}sPageCursor, {item}>"
            self.types.setdefault(f"{stem}sPageCursor", f"PageCursor<{item}>")
            body = f"    return this._client.getAPIList({route}, PageCursor<{item}>, {{ {init} }});\n"
        else:
            ret = f"APIPromise<{self.alias(op.response)}>"
            verb = {"get": "get", "post": "post", "put": "put", "patch": "patch", "delete": "delete"}[op.verb]
            body = f"    return this._client.{verb}({route}, {{ {init} }});\n"
        return doc(op) + f"  {name}({', '.join(args)}): {ret} {{\n{body}  }}\n"

    def service(self, svc: Service) -> str:
        out = [f"export class {class_name(svc)} extends APIResource {{"]
        for child in self.m.children(svc.path):
            out.append(f"  {prop_name(child)}: {class_name(child)} = new {class_name(child)}(this._client);\n")
        out.append("\n".join(self.method(svc, op) for op in svc.ops))
        out.append("}\n")
        return "\n".join(out)

    def run(self) -> tuple[str, str]:
        classes = [self.service(s) for s in self.m.services.values()]
        header = (
            "// Code generated by tools/sdkgen/ts2gen.py from contracts/bma/v2/extensions.openapi.yaml; DO NOT EDIT.\n\n"
            "import { APIPromise } from '@anthropic-ai/sdk/core/api-promise';\n"
            "import { PageCursor, PagePromise } from '@anthropic-ai/sdk/core/pagination';\n"
            "import type { BaseAnthropic } from '@anthropic-ai/sdk/client';\nimport { APIResource } from '@anthropic-ai/sdk/core/resource';\n"
            "import { mergeHeaders, path, type RequestOptions } from '../internal.js';\n"
            "import { newIdempotencyKey } from '../idempotency.js';\n"
            "import type { components } from './extensions.js';\n\n"
            "type S = components['schemas'];\n\n"
        )
        types = "".join(f"export type {n} = {e};\n" for n, e in sorted(self.types.items()))
        roots = [s for s in self.m.roots() if "." not in s.path]
        wiring = "export interface ExtensionServices {\n" + "".join(
            f"  {prop_name(s)}: {class_name(s)};\n" for s in roots
        ) + "}\n\nexport function newExtensionServices(client: BaseAnthropic): ExtensionServices {\n  return {\n" + "".join(
            f"    {prop_name(s)}: new {class_name(s)}(client),\n" for s in roots
        ) + "  };\n}\n"
        return header + types + "\n" + "\n".join(self.params) + "\n" + "\n".join(classes) + "\n" + wiring, ""


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__, file=sys.stderr)
        return 2
    contract, resources, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    text, _ = Gen(Model(contract, resources)).run()
    target = out / "extensions-resources.ts"
    target.write_text(text)
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
