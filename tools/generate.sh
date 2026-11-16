#!/usr/bin/env bash
# Regenerate every SDK surface from contracts/bma/*.openapi.yaml.
#
# Requires: python3 with PyYAML, Go 1.25+, Node 20+ with npm, and uv. The
# generator versions are pinned here and in typescript/package-lock.json.
# Generated files must never be edited by hand.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

OAPI_CODEGEN=github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen@v2.7.0
RUFF=ruff==0.17.4

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

# Go: oapi-codegen models, then the resource layer (ADR 0012) from their
# struct fields; fails when an operation is missing from sdk.resources.yaml.
go_resources() { # <contract> <section> <models.go> <resources.go> <package>
  local fields
  fields="$(mktemp)"
  go run ./tools/sdkgen/gofields "$3" > "$fields"
  python3 tools/sdkgen/sdkgen.py go "$1" "$2" contracts/bma/sdk.resources.yaml "$4" --fields "$fields" --package "$5"
  rm -f "$fields"
  gofmt -w "$4"
}
go_generate contracts/bma/rest.openapi.yaml tools/oapi-rest.yaml generated_models.go
go_resources contracts/bma/rest.openapi.yaml rest generated_models.go generated_resources.go bma
go_generate contracts/bma/facade-extensions.openapi.yaml tools/oapi-facadeext.yaml facade/generated_models.go
go_resources contracts/bma/facade-extensions.openapi.yaml facade facade/generated_models.go facade/generated_resources.go facade

# Go 3.0 (module v3/): extension models, then the extension services; the
# shared Claude Managed Agents resources are the official anthropic-sdk-go
# services (ADR 0025). The model input keeps only components.schemas:
# parameter and response types would collide with Page[T] and Error.
contract=contracts/bma/v3/extensions.openapi.yaml
python3 tools/downgrade_openapi.py "$contract" .build/extensions.openapi.3.0.yaml
python3 - .build/extensions.openapi.3.0.yaml <<'PY'
import sys, yaml
doc = yaml.safe_load(open(sys.argv[1]))
# Preserve the public Go value field while the current source makes it optional.
# Empty SecretID is invalid on the wire; omitempty represents absence.
doc["components"]["schemas"]["CreateMachinePoolRequestBase"]["properties"]["provider_auth_secret_id"]["x-go-type-skip-optional-pointer"] = True
for key in ("parameters", "responses"):
    doc["components"].pop(key, None)
doc["paths"] = {}
yaml.safe_dump(doc, open(sys.argv[1], "w"), sort_keys=False, width=1000)
PY
models_tmp="$(mktemp)"
go run "$OAPI_CODEGEN" -config tools/oapi-extensions.yaml .build/extensions.openapi.3.0.yaml > "$models_tmp"
{
  echo "// Code generated from $contract by tools/generate.sh; DO NOT EDIT."
  echo
  cat "$models_tmp"
} > v3/generated_models.go
rm -f "$models_tmp"
gofmt -w v3/generated_models.go
python3 tools/sdkgen/go2gen.py "$contract" contracts/bma/v3/sdk.resources.yaml \
  v3/generated_models.go v3/generated_resources.go
gofmt -w v3/generated_resources.go
echo "wrote v3/generated_models.go v3/generated_resources.go"

# TypeScript: schema types from openapi-typescript (a default makes a field
# required only outside request bodies, see tools/ts_request_defaults.py), then
# the extension services on the official client.
python3 tools/ts_request_defaults.py "$contract" .build/extensions.openapi.ts.yaml
(cd typescript && npm ci --silent && npm run --silent generate)
python3 tools/sdkgen/ts2gen.py "$contract" contracts/bma/v3/sdk.resources.yaml typescript/src/generated
echo "wrote typescript/src/generated"

# Python: models, request types and the extension services on the
# official client, formatted.
python3 tools/sdkgen/py2gen.py "$contract" contracts/bma/v3/sdk.resources.yaml python/src/bma_sdk/_generated
uvx --quiet "$RUFF" format --quiet --line-length 120 python/src/bma_sdk/_generated
