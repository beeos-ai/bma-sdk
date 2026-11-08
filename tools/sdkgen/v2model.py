"""The extension operations of contracts/bma/v2/extensions.openapi.yaml as the
TypeScript and Python generators (ts2gen.py, py2gen.py) see them.

The resource map contracts/bma/v2/sdk.resources.yaml names the Go methods
(New, Get, ...); the other SDKs follow their official SDK instead: New is
create and Get is retrieve (anthropic-sdk-typescript and anthropic-sdk-python
name them that way), every other method is its name in the language's case.
Generation fails on an operation that is not mapped (ADR 0012 D1).
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

METHODS = ("get", "post", "put", "patch", "delete")
OFFICIAL_NAMES = {"New": "create", "Get": "retrieve"}
IDEMPOTENCY_HEADER = "Idempotency-Key"


def words(snake: str) -> list[str]:
    return [p for p in snake.split("_") if p]


def camel_case(snake: str) -> str:
    parts = words(snake)
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


def pascal_case(snake: str) -> str:
    return "".join(p[:1].upper() + p[1:] for p in words(snake))


def pascal_to_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def ref_name(schema: dict) -> str | None:
    ref = schema.get("$ref")
    return ref.rsplit("/", 1)[-1] if ref else None


@dataclass
class Query:
    name: str
    schema: dict[str, Any]
    required: bool
    description: str


@dataclass
class Op:
    op_id: str
    verb: str
    path: str
    summary: str
    description: str
    service: str  # path under client.beta, e.g. MachinePools.Grants
    method: str  # official-style PascalCase: New, Get, Update, List, AcquireControl
    path_params: list[str]
    queries: list[Query]
    body: str | None  # request schema name
    body_required: bool
    response: str  # response schema name (the item schema for a list)
    paged: bool
    idempotent: bool


@dataclass
class Service:
    path: str
    stem: str
    ops: list[Op] = field(default_factory=list)


class Model:
    def __init__(self, contract: Path, resources: Path):
        self.doc = yaml.safe_load(contract.read_text())
        self.res = yaml.safe_load(resources.read_text())
        self.schemas: dict[str, Any] = self.doc["components"]["schemas"]
        self.params: dict[str, Any] = self.doc["components"].get("parameters", {})
        self.skip_query = set(self.res.get("skip_query", []))
        self.services: dict[str, Service] = {p: Service(p, stem) for p, stem in self.res["services"].items()}
        self.operations = self.collect()

    def deref(self, node: Any) -> Any:
        while isinstance(node, dict) and "$ref" in node:
            target: Any = self.doc
            for part in node["$ref"].removeprefix("#/").split("/"):
                target = target[part]
            node = target
        return node

    def collect(self) -> list[Op]:
        mapping: dict[str, str] = self.res["operations"]
        seen: set[str] = set()
        out: list[Op] = []
        for path, item in self.doc["paths"].items():
            for verb in METHODS:
                raw = item.get(verb)
                if not isinstance(raw, dict):
                    continue
                op_id = raw["operationId"]
                seen.add(op_id)
                target = mapping.get(op_id) or sys.exit(f"operation {op_id} is not in sdk.resources.yaml")
                if target == "official":
                    continue
                service, method = target.rsplit(".", 1)
                if service not in self.services:
                    sys.exit(f"{op_id}: unknown service {service}")
                op = self.operation(op_id, verb, path, raw, service, method)
                self.services[service].ops.append(op)
                out.append(op)
        stale = set(mapping) - seen
        if stale:
            sys.exit(f"sdk.resources.yaml maps operations the contract does not have: {sorted(stale)}")
        return out

    def operation(self, op_id: str, verb: str, path: str, raw: dict, service: str, method: str) -> Op:
        params = [self.deref(p) for p in raw.get("parameters", [])]
        queries = [
            Query(
                p["name"],
                self.deref(p.get("schema", {})),
                bool(p.get("required")),
                (p.get("description") or p.get("schema", {}).get("description") or "").strip(),
            )
            for p in params
            if p["in"] == "query" and p["name"] not in self.skip_query
        ]
        idempotent = any(p["in"] == "header" and p["name"] == IDEMPOTENCY_HEADER for p in params)
        body = raw.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema")
        if body and queries:
            sys.exit(f"{op_id}: body and query parameters together are not supported")
        body_name = None
        if body:
            body_name = ref_name(body) or sys.exit(f"{op_id}: inline request body")
        ok = [c for c in raw["responses"] if str(c).startswith("2")]
        schema = raw["responses"][ok[0]].get("content", {}).get("application/json", {}).get("schema")
        response = (ref_name(schema) if schema else None) or sys.exit(f"{op_id}: no $ref JSON response")
        props = self.schemas[response].get("properties", {})
        paged = set(props) == {"data", "next_page"}
        if paged:
            response = ref_name(props["data"]["items"]) or sys.exit(f"{op_id}: inline list item")
        return Op(
            op_id=op_id,
            verb=verb,
            path=path,
            summary=raw.get("summary", "").strip().rstrip("."),
            description=" ".join(raw.get("description", "").split()),
            service=service,
            method=method,
            path_params=re.findall(r"{(\w+)}", path),
            queries=queries,
            body=body_name,
            body_required=bool(body_name and self.body_has_required(body_name)),
            response=response,
            paged=paged,
            idempotent=idempotent,
        )

    def body_has_required(self, name: str) -> bool:
        schema = self.deref(self.schemas[name])
        if schema.get("required"):
            return True
        if any(self.deref(s).get("required") for s in schema.get("allOf", [])):
            return True
        branches = schema.get("oneOf") or schema.get("anyOf")
        return bool(branches) and all(self.deref(b).get("required") for b in branches)

    def method_name(self, op: Op, case: str) -> str:
        """Method name in the SDK's case: `camel` or `snake`."""
        name = OFFICIAL_NAMES.get(op.method)
        if name is None:
            name = pascal_to_snake(op.method)
            return name if case == "snake" else camel_case(name)
        return name

    def children(self, path: str) -> list[Service]:
        return [s for p, s in self.services.items() if p.rsplit(".", 1)[0] == path and "." in p]

    def roots(self) -> list[Service]:
        """Services whose parent is not itself a generated service: they are
        wired by hand (Organization.Projects) or are top-level."""
        return [s for p, s in self.services.items() if "." not in p or p.rsplit(".", 1)[0] not in self.services]
