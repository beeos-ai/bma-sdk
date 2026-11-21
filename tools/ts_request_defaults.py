#!/usr/bin/env python3
"""Materialize the contract openapi-typescript reads, so a default only makes a
field required where the server fills it in.

openapi-typescript (defaultNonNullable, on by default) emits a property that
has a `default` as required, because the server always returns it, except
under an inline `requestBody` or `parameters`. Our request bodies are
`$ref`s to component schemas, so that exception never applies and optional
request fields with a default (e.g. `CreateMemoryStore.agent_access`) became
required in the TypeScript params.

TypeScript is therefore generated with `--default-non-nullable=false` (a field
is required only when the contract lists it in `required`), from a copy in
which every schema that is not part of a request body lists its defaulted
properties in `required`: response types keep their current shape and request
fields with a default become optional, as the contract (and the Python and Go
SDKs) already treat them. A component schema used by both a request and a
response cannot be both, so it fails the generation.

Usage: `python3 tools/ts_request_defaults.py <source.yaml> <target.yaml>`.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

SCHEMA_REF = "#/components/schemas/"


def resolve(doc: dict, node: object) -> object:
    while isinstance(node, dict) and "$ref" in node:
        target = doc
        for key in node["$ref"].removeprefix("#/").split("/"):
            target = target[key]
        node = target
    return node


def referenced(doc: dict, node: object, found: set[str]) -> set[str]:
    """Component schemas reachable from node, following $refs transitively."""
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str) and ref.startswith(SCHEMA_REF):
            name = ref.removeprefix(SCHEMA_REF)
            if name not in found:
                found.add(name)
                referenced(doc, doc["components"]["schemas"][name], found)
        elif isinstance(ref, str):
            referenced(doc, resolve(doc, node), found)
        for value in node.values():
            referenced(doc, value, found)
    elif isinstance(node, list):
        for value in node:
            referenced(doc, value, found)
    return found


def defaulted_optional(schema: dict) -> list[str]:
    props = schema.get("properties")
    if not isinstance(props, dict):
        return []
    required = schema.get("required") or []
    return [k for k, v in props.items() if isinstance(v, dict) and "default" in v and k not in required]


def require_defaults(node: object) -> None:
    """List defaulted properties as required in every schema under node.
    $refs are not followed: component schemas are handled by name."""
    if isinstance(node, list):
        for value in node:
            require_defaults(value)
        return
    if not isinstance(node, dict):
        return
    missing = defaulted_optional(node)
    if missing:
        node["required"] = [*(node.get("required") or []), *missing]
    for value in node.values():
        require_defaults(value)


def main(source: str, target: str) -> None:
    doc = yaml.safe_load(Path(source).read_text())
    schemas = doc.get("components", {}).get("schemas", {})
    request: set[str] = set()
    response: set[str] = set()
    for item in doc.get("paths", {}).values():
        for op in item.values():
            if not isinstance(op, dict):
                continue
            if "requestBody" in op:
                referenced(doc, op["requestBody"], request)
            referenced(doc, op.get("responses"), response)

    shared = sorted(n for n in request & response if defaulted_optional(schemas[n]))
    if shared:
        raise SystemExit(
            f"{source}: schemas used in both requests and responses have optional fields with a default "
            f"(split the schema or list the fields in required): {', '.join(shared)}"
        )

    for name, schema in schemas.items():
        if name not in request:
            require_defaults(schema)
    for item in doc.get("paths", {}).values():
        for op in item.values():
            if isinstance(op, dict):
                require_defaults(op.get("responses"))
    require_defaults(doc.get("components", {}).get("responses"))

    Path(target).parent.mkdir(parents=True, exist_ok=True)
    Path(target).write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
