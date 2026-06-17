#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BOOT="$SKILL_DIR/scripts/bootstrap_agentic_repo.py"

echo "== unit: self-check =="
python3 "$BOOT" --self-check

echo "== unit: dry-run writes nothing =="
TMP_DRY="$(mktemp -d)"
trap 'rm -rf "$TMP_DRY" "${TMP:-}"' EXIT
python3 "$BOOT" --mode greenfield --target "$TMP_DRY" --dry-run >/dev/null
test -z "$(ls -A "$TMP_DRY")" || { echo "FAIL: dry-run created files"; exit 1; }

echo "== integration: greenfield bootstrap + make verify =="
command -v uv >/dev/null || { echo "SKIP: uv not installed"; exit 0; }
TMP="$(mktemp -d)"
python3 "$BOOT" --mode greenfield --project-name "Test Proj" --pkg testproj --target "$TMP"
( cd "$TMP" && git init -q && make verify )

echo "== no-clobber: rerun skips =="
OUT="$(python3 "$BOOT" --mode greenfield --pkg testproj --target "$TMP")"
echo "$OUT" | grep -q "skipped" || { echo "FAIL: rerun did not skip"; exit 1; }

echo "INTEGRATION OK"
