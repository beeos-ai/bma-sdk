#!/usr/bin/env python3
"""Materialize the SDK-facing REST contract in OpenAPI 3.0.3 form.

`contracts/bma/rest.openapi.yaml` is authored as OpenAPI 3.1.2 by the private
BMA repository. oapi-codegen v2 targets OpenAPI 3.0, so this script applies the
small, mechanical downgrade the contract uses:

* `type: [T, "null"]` -> `type: T` with `nullable: true`
* single-value `const: x` -> `enum: [x]`
* `anyOf`/`oneOf` null-only branches -> `nullable: true` on the parent
* `unevaluatedProperties` removed (composition is flattened differently in 3.0)
* schema `examples: [x]` -> `example: x`
* backend-only `x-go-type*` extensions removed: they point at private packages
  and must never leak into a public SDK.

The script intentionally refuses unknown unions rather than guessing. Run it
from the repository root: `python3 tools/downgrade_openapi.py`.
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "contracts" / "bma" / "rest.openapi.yaml"
TARGET = ROOT / ".build" / "rest.openapi.3.0.yaml"

DROP_EXTENSIONS = {
    "x-go-type",
    "x-go-type-import",
    "x-go-type-skip-optional-pointer",
}


def simplify_unions(node: object, stats: Counter) -> None:
    if isinstance(node, list):
        for item in node:
            simplify_unions(item, stats)
        return
    if not isinstance(node, dict):
        return

    for key in ("anyOf", "oneOf"):
        branches = node.get(key)
        if not isinstance(branches, list):
            continue
        nulls = [
            b
            for b in branches
            if isinstance(b, dict) and b.get("type") == "null" and len(b) == 1
        ]
        if not nulls:
            continue
        non_null = [b for b in branches if b not in nulls]
        if not non_null:
            raise SystemExit(f"unsupported null-only {key} at {node!r}")
        stats[f"{key}_with_null"] += 1
        if len(non_null) == 1 and isinstance(non_null[0], dict):
            for k, v in non_null[0].items():
                node.setdefault(k, v)
            del node[key]
        else:
            node[key] = non_null
        node["nullable"] = True

    for key in DROP_EXTENSIONS:
        if key in node:
            del node[key]
            stats["dropped_backend_extension"] += 1

    for value in node.values():
        simplify_unions(value, stats)


def main() -> int:
    if not SOURCE.is_file():
        print(f"missing contract: {SOURCE}", file=sys.stderr)
        return 1

    document = yaml.safe_load(SOURCE.read_text(encoding="utf-8"))
    version = str(document.get("openapi", ""))
    if not version.startswith("3.1."):
        print(f"expected OpenAPI 3.1.x contract, got {version!r}", file=sys.stderr)
        return 1

    stats: Counter = Counter()

    # Union simplification can expose a type array and vice versa; iterate to a
    # fixed point and fail if the contract keeps changing.
    for _ in range(8):
        before = (
            stats["type_list"],
            stats["const"],
            stats["union_with_null"],
        )
        simplify_unions(document, stats)
        if _walk_schemas(document, stats) == 0:
            print(f"unsupported schema construct: {stats}", file=sys.stderr)
            return 1
        after = (
            stats["type_list"],
            stats["const"],
            stats["union_with_null"],
        )
        if before == after:
            break
    else:
        print("contract did not converge", file=sys.stderr)
        return 1

    document["openapi"] = "3.0.3"
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with TARGET.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(
            document,
            handle,
            sort_keys=False,
            allow_unicode=True,
            width=1000,
        )

    print(
        "wrote "
        f"{TARGET.relative_to(ROOT)} "
        f"(type arrays={stats['type_list']}, consts={stats['const']}, "
        f"nullable unions={stats['union_with_null']}, "
        f"stripped backend extensions={stats['dropped_backend_extension']})"
    )
    return 0


def _walk_schemas(node: object, stats: Counter) -> int:
    """Convert the remaining 3.1 schema keywords; returns 0 when unsupported."""
    if isinstance(node, list):
        return all(_walk_schemas(item, stats) for item in node)
    if not isinstance(node, dict):
        return 1

    node_type = node.get("type")
    if isinstance(node_type, list):
        non_null = [value for value in node_type if value != "null"]
        if len(non_null) != 1:
            return 0
        node["type"] = non_null[0]
        if "null" in node_type:
            node["nullable"] = True
        stats["type_list"] += 1
    elif node_type == "null":
        node.pop("type")
        node["nullable"] = True

    if "const" in node:
        node.setdefault("enum", [node["const"]])
        del node["const"]
        stats["const"] += 1

    if "unevaluatedProperties" in node:
        del node["unevaluatedProperties"]
        stats["unevaluatedProperties"] += 1

    if isinstance(node.get("examples"), list):
        node.setdefault("example", node["examples"][0])
        del node["examples"]
        stats["examples"] += 1

    for value in node.values():
        if not _walk_schemas(value, stats):
            return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
