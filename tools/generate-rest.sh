#!/usr/bin/env bash
# Regenerate go/rest/generated.go from the committed REST contract.
#
# Requires: python3 with PyYAML, Go 1.24+, network access for the pinned
# oapi-codegen module (cached after the first run).
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

python3 tools/downgrade_openapi.py

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT
go run github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@v2.7.0 \
  -config tools/oapi-config.yaml \
  .build/rest.openapi.3.0.yaml > "$tmp"

{
  echo '// Code generated from contracts/bma/rest.openapi.yaml by tools/generate-rest.sh; DO NOT EDIT.'
  echo
  cat "$tmp"
} > go/rest/generated.go
gofmt -w go/rest/generated.go

echo "wrote go/rest/generated.go"
