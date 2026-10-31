# BMA contracts

| File | What it is |
| --- | --- |
| `rest.openapi.yaml` | Byte-for-byte snapshot of `backend/api/openapi/openapi.yaml` in `beeos-ai/beeos-managed-agents` (the native `/api/v1` API). Commit and sha256 are in `lock.json`. |
| `facade-extensions.openapi.yaml` | The BMA extensions to the Anthropic Managed Agents facade, written from `backend/internal/managedagents/{server,desktop,files,types,sessions}.go`. Standard Anthropic routes are not described here; use the official Anthropic SDKs for them. |
| `lock.json` | Source commit, REST snapshot sha256, and every facade route registered in `server.go`, classified `anthropic` or `bma_extension`. |
| `fixtures/sdk-contract.json` | Recorded request/response pairs replayed by the Go, TypeScript and Python tests. |

All generated SDK code comes from the two OpenAPI files via `tools/generate.sh`.
Never edit generated files by hand.

## Refreshing the contract

```bash
bma=../beeos-managed-agents            # checkout of beeos-ai/beeos-managed-agents
git -C "$bma" fetch origin main
git -C "$bma" show origin/main:backend/api/openapi/openapi.yaml > contracts/bma/rest.openapi.yaml
# update lock.json: source_commit, rest.sha256, and facade.routes when server.go changed
./tools/generate.sh
python3 tools/check_contract.py --source "$bma"
```

`tools/check_contract.py` without `--source` runs in CI: lock hash, facade
route classification, fixture validation against the schemas, and operation
coverage in all three SDKs. `--source` also proves the snapshot and the facade
routes match the server at `--ref` (default `origin/main`); the upstream
repository is private, so that step runs on a release machine.
