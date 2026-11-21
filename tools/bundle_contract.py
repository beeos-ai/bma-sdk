#!/usr/bin/env python3
"""Snapshot the public BMA contract for bma-sdk 4.0.

`api/openapi/bma.openapi.yaml` in beeos-ai/beeos-managed-agents is the whole
public API (official Claude Managed Agents operations and BMA extensions,
`x-bma-extension`), self-contained and equal to the gateway's public routes.
This copies it byte for byte and records the source commit and sha256:

  contracts/bma/v4/bma.openapi.yaml
  contracts/bma/v4/lock.json

The upstream repository is private, so this runs on a machine with a checkout:

  python3 tools/bundle_contract.py --source ../beeos-managed-agents [--ref origin/main]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "contracts/bma/v4"
SOURCE_PATH = "api/openapi/bma.openapi.yaml"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--ref", default="origin/main")
    args = parser.parse_args()

    def git(*cmd: str) -> bytes:
        return subprocess.run(["git", "-C", str(args.source), *cmd], check=True, capture_output=True).stdout

    commit = git("rev-parse", args.ref).decode().strip()
    raw = git("show", f"{commit}:{SOURCE_PATH}")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "bma.openapi.yaml").write_bytes(raw)
    lock = {
        "source_repository": "beeos-ai/beeos-managed-agents",
        "source_commit": commit,
        "source_path": SOURCE_PATH,
        "contract": "contracts/bma/v4/bma.openapi.yaml",
        "sha256": hashlib.sha256(raw).hexdigest(),
    }
    (OUT / "lock.json").write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT / 'bma.openapi.yaml'} from {commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
