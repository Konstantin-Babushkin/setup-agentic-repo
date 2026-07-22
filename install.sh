#!/usr/bin/env bash
set -euo pipefail

REPO="https://github.com/maddevsio/agent-scaffold.git"
NAME="agent-scaffold"
TARGETS=(
  "$HOME/.claude/skills/$NAME"
  "$HOME/.codex/skills/$NAME"
  "$HOME/.cursor/skills/$NAME"
)

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --depth 1 "$REPO" "$TMP/$NAME" >/dev/null 2>&1
rm -rf "$TMP/$NAME/.git"

for dir in "${TARGETS[@]}"; do
  mkdir -p "$(dirname "$dir")"
  rm -rf "$dir"
  cp -r "$TMP/$NAME" "$dir"
  echo "installed -> $dir"
done

echo "reload your agent CLI/IDE to pick up $NAME"
