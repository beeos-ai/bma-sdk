#!/usr/bin/env bash
# Regenerate every SDK surface from contracts/bma/*.openapi.yaml.
#
# Requires: python3 with PyYAML, Go 1.24+, Node 20+ with npm, and uv. The
# generator versions are pinned here and in typescript/package-lock.json.
# Generated files must never be edited by hand.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

OAPI_CODEGEN=github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@v2.7.0
PY_CLIENT=openapi-python-client==0.26.2

go_generate() { # <contract> <config> <output>
  local name tmp
  name="$(basename "$1" .yaml)"
  python3 tools/downgrade_openapi.py "$1" ".build/$name.3.0.yaml"
  tmp="$(mktemp)"
  go run "$OAPI_CODEGEN" -config "$2" ".build/$name.3.0.yaml" > "$tmp"
  {
    echo "// Code generated from $1 by tools/generate.sh; DO NOT EDIT."
    echo
    cat "$tmp"
  } > "$3"
  rm -f "$tmp"
  gofmt -w "$3"
  echo "wrote $3"
}

py_generate() { # <contract> <package dir>
  local log
  log="$(mktemp)"
  rm -rf "$2"
  # The generator warns about the daemon-only text/plain and */* binary
  # operations; those are covered by hand-written code or exempted in
  # tools/check_contract.py. Show its output only when it fails.
  if ! uvx --from "$PY_CLIENT" openapi-python-client generate \
    --path "$1" --output-path "$2" --meta none \
    --config tools/openapi-python-client.yaml >"$log" 2>&1; then
    cat "$log" >&2
    rm -f "$log"
    return 1
  fi
  rm -f "$log"
  echo "wrote $2"
}

go_generate contracts/bma/rest.openapi.yaml tools/oapi-rest.yaml go/rest/generated.go
go_generate contracts/bma/facade-extensions.openapi.yaml tools/oapi-facadeext.yaml go/facadeext/generated.go

(cd typescript && npm ci --silent && npm run --silent generate)
echo "wrote typescript/src/generated"

py_generate contracts/bma/rest.openapi.yaml python/src/bma_sdk/rest
py_generate contracts/bma/facade-extensions.openapi.yaml python/src/bma_sdk/facade_extensions/_generated
