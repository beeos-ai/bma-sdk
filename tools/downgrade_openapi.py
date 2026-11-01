#!/usr/bin/env python3
"""Materialize an SDK-facing contract in OpenAPI 3.0.3 form.

The contracts under `contracts/bma/` are authored as OpenAPI 3.1.2.
oapi-codegen v2 targets OpenAPI 3.0, so this script applies the small,
mechanical downgrade the contracts use:

* `type: [T, "null"]` -> `type: T` with `nullable: true`
* single-value `const: x` -> `enum: [x]`
* `anyOf`/`oneOf` null-only branches -> `nullable: true` on the parent
* `unevaluatedProperties` removed (composition is flattened differently in 3.0)
* schema `examples: [x]` -> `example: x`
* backend-only `x-go-type*` extensions removed: they point at private packages
  and must never leak into a public SDK.

The script intentionally refuses unknown unions rather than guessing. Usage:
`python3 tools/downgrade_openapi.py <source.yaml> <target.yaml>`.
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import yaml


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
            branch = non_null[0]
            if "$ref" in branch:
                # OpenAPI 3.0 ignores keywords next to `$ref`, so a bare
                # `nullable: true` would be dropped and the field generated
                # as a non-pointer. Wrap the reference instead.
                node[key] = [branch]
                node["allOf"] = node.pop(key)
                stats["nullable_ref"] += 1
            else:
                for k, v in branch.items():
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
    if len(sys.argv) != 3:
        print("usage: downgrade_openapi.py <source.yaml> <target.yaml>", file=sys.stderr)
        return 2
    SOURCE, TARGET = Path(sys.argv[1]), Path(sys.argv[2])
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
        f"{TARGET} "
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
