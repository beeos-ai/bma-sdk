#!/usr/bin/env python3
"""Derive the generator input for the BMA extensions from the public contract.

contracts/bma/v4/bma.openapi.yaml is the whole public BMA API: the operations
BMA shares with Claude Managed Agents (`x-bma-extension: false`, served by the
official anthropic-sdk-go / @anthropic-ai/sdk / anthropic clients) and the BMA
extensions (`x-bma-extension: true`). The SDK generates only the extensions,
so this keeps the extension operations, rebases their paths on the `/v1`
server, and keeps only the schemas, parameters and responses they (or the
documented extension fields) reach.

  python3 tools/sdkgen/extensions_input.py <bma.openapi.yaml> <out.yaml>
"""
from __future__ import annotations

import sys

import yaml

METHODS = ("get", "post", "put", "patch", "delete")
PREFIX = "/v1"


def refs(node, out: set[str]) -> None:
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str):
            out.add(ref)
        for value in node.values():
            refs(value, out)
    elif isinstance(node, list):
        for item in node:
            refs(item, out)


def official_schemas(doc: dict) -> set[str]:
    """The component schemas the official operations answer with."""
    out: set[str] = set()
    for item in doc["paths"].values():
        for method in METHODS:
            op = item.get(method)
            if not isinstance(op, dict) or op.get("x-bma-extension") is not False:
                continue
            for code, r in op.get("responses", {}).items():
                ref = r.get("content", {}).get("application/json", {}).get("schema", {}).get("$ref", "")
                if str(code).startswith("2") and ref:
                    out.add(ref.rsplit("/", 1)[-1])
    return out


def extensions(doc: dict) -> dict:
    paths: dict = {}
    for path, item in doc["paths"].items():
        ops = {m: item[m] for m in METHODS if m in item and item[m].get("x-bma-extension") is True}
        if not ops:
            continue
        if not path.startswith(PREFIX + "/"):
            raise SystemExit(f"extension path {path} is not under {PREFIX}")
        shared = {k: v for k, v in item.items() if k not in METHODS}
        paths[path[len(PREFIX):]] = {**shared, **ops}

    components = doc["components"]
    # An extension operation that answers an official object (a fork answers a
    # session) answers it as the official SDK's type: the generators read
    # x-bma-official-response, and the official schema is not generated again.
    official = official_schemas(doc)
    for item in paths.values():
        for method in METHODS:
            op = item.get(method)
            if not op:
                continue
            for code, r in op["responses"].items():
                media = r.get("content", {}).get("application/json") if str(code).startswith("2") else None
                name = (media or {}).get("schema", {}).get("$ref", "").rsplit("/", 1)[-1]
                if name in official:
                    op["x-bma-official-response"] = name
                    del r["content"]
    # The generators name every request and response type after a component:
    # an inline JSON body becomes <OperationId>Request / <OperationId>Response.
    for item in paths.values():
        for method in METHODS:
            if method not in item:
                continue
            op = item[method]
            stem = op["operationId"][:1].upper() + op["operationId"][1:]
            bodies = [("Request", op.get("requestBody", {}))]
            bodies += [("Response", r) for code, r in op["responses"].items() if str(code).startswith("2")]
            for suffix, holder in bodies:
                media = holder.get("content", {}).get("application/json")
                if media and "$ref" not in media.get("schema", {"$ref": None}):
                    name = stem + suffix
                    if name in components["schemas"]:
                        raise SystemExit(f"{op['operationId']}: schema {name} already exists")
                    components["schemas"][name] = media["schema"]
                    media["schema"] = {"$ref": f"#/components/schemas/{name}"}
    kept: dict[str, dict] = {section: {} for section in ("schemas", "parameters", "responses")}
    pending: set[str] = set()
    refs(paths, pending)
    refs(doc.get("x-bma-extension-fields", []), pending)
    while pending:
        ref = pending.pop()
        _, _, section, name = ref.split("/", 3)
        if name in kept[section]:
            continue
        kept[section][name] = components[section][name]
        refs(components[section][name], pending)

    out = {k: v for k, v in doc.items() if k not in ("paths", "components", "servers")}
    out["servers"] = [{"url": PREFIX}]
    out["paths"] = paths
    out["components"] = {"securitySchemes": components["securitySchemes"]}
    for section in ("parameters", "responses", "schemas"):
        out["components"][section] = {name: kept[section][name] for name in components[section] if name in kept[section]}
    return out


def main() -> int:
    source, target = sys.argv[1:3]
    doc = extensions(yaml.safe_load(open(source, encoding="utf-8")))
    with open(target, "w", encoding="utf-8") as handle:
        yaml.safe_dump(doc, handle, sort_keys=False, allow_unicode=True, width=1000)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
