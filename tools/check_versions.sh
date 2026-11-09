#!/usr/bin/env bash
# Every SDK version must be the same: typescript/package.json (npm),
# python/pyproject.toml (PyPI; the Python client reads it from the installed
# metadata), the TypeScript and Go 2.0 version constants, and, when given, the
# release tag (vX.Y.Z; the Go module version is the tag itself). The Go 1.x
# module at the repository root is frozen (it stays at 1.x and is not part of
# a release); Go 2.0 is the module in v2/.
#   tools/check_versions.sh [vX.Y.Z]
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

declare -A found
found[typescript/package.json]="$(node -p "require('./typescript/package.json').version")"
found[typescript/package-lock.json]="$(node -p "require('./typescript/package-lock.json').version")"
found[python/pyproject.toml]="$(python3 -c 'import tomllib; print(tomllib.load(open("python/pyproject.toml", "rb"))["project"]["version"])')"
found[typescript/src/version.ts]="$(sed -n 's/^export const SDK_VERSION = "\(.*\)";$/\1/p' typescript/src/version.ts)"
found[v2/client.go]="$(sed -n 's/^[[:space:]]*SDKVersion = "\(.*\)"$/\1/p' v2/client.go)"
want="${1:-}"; want="${want#v}"
[ -n "${1:-}" ] || want="${found[typescript/package.json]}"
# No pre-release or build suffix anywhere (beeos-versioning).
if ! [[ "$want" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  printf 'release version "%s" must be plain X.Y.Z (no pre-release suffix)\n' "$want" >&2
  exit 1
fi
status=0
for file in "${!found[@]}"; do
  if [ "${found[$file]}" != "$want" ]; then
    printf '%s has version "%s", want %s\n' "$file" "${found[$file]}" "$want" >&2
    status=1
  fi
done
[ "$status" = 0 ] && echo "versions: all $want"
exit "$status"
