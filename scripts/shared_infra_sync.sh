#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  scripts/shared_infra_sync.sh --mode <bootstrap|refresh> --target-root <path> [--shared-root <path>]

Description:
  Copies shared-infra baseline assets into a target repository.
  - bootstrap: creates missing files/directories only (non-destructive).
  - refresh: updates shared-managed assets and writes backups for changed files.
USAGE
}

MODE=""
TARGET_ROOT=""
SHARED_ROOT="."

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      MODE="${2:-}"
      shift 2
      ;;
    --target-root)
      TARGET_ROOT="${2:-}"
      shift 2
      ;;
    --shared-root)
      SHARED_ROOT="${2:-}"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1"
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$MODE" || -z "$TARGET_ROOT" ]]; then
  usage
  exit 1
fi

if [[ "$MODE" != "bootstrap" && "$MODE" != "refresh" ]]; then
  echo "Invalid --mode: $MODE (expected bootstrap|refresh)"
  exit 1
fi

SHARED_ROOT="$(cd "$SHARED_ROOT" && pwd)"
TARGET_ROOT="$(cd "$TARGET_ROOT" && pwd)"

if [[ ! -d "$TARGET_ROOT" ]]; then
  echo "Target root does not exist: $TARGET_ROOT"
  exit 1
fi

copy_file() {
  local src="$1"
  local dst="$2"
  mkdir -p "$(dirname "$dst")"

  if [[ "$MODE" == "bootstrap" ]]; then
    if [[ -e "$dst" ]]; then
      echo "SKIP (exists): $dst"
      return 0
    fi
    cp -f "$src" "$dst"
    echo "ADD: $dst"
    return 0
  fi

  if [[ -e "$dst" ]] && ! cmp -s "$src" "$dst"; then
    local ts
    ts="$(date -u +%Y%m%dT%H%M%SZ)"
    cp -f "$dst" "$dst.shared-infra.bak.$ts"
    echo "BACKUP: $dst.shared-infra.bak.$ts"
  fi

  cp -f "$src" "$dst"
  echo "SYNC: $dst"
}

copy_persona_if_missing_or_warn() {
  local src="$1"
  local dst="$2"
  mkdir -p "$(dirname "$dst")"

  if [[ ! -e "$dst" ]]; then
    cp -f "$src" "$dst"
    echo "ADD: $dst"
    return 0
  fi

  if ! cmp -s "$src" "$dst"; then
    echo "SKIP (persona differs, not overwritten): $dst"
    return 0
  fi

  echo "SKIP (persona unchanged): $dst"
}

sync_tree() {
  local src_dir="$1"
  local dst_dir="$2"

  if [[ ! -d "$src_dir" ]]; then
    echo "WARN: source tree missing: $src_dir"
    return 0
  fi

  mkdir -p "$dst_dir"

  while IFS= read -r -d '' src_file; do
    local rel
    rel="${src_file#"$src_dir"/}"

    case "$rel" in
      */__pycache__/*|*.pyc)
        continue
        ;;
    esac

    copy_file "$src_file" "$dst_dir/$rel"
  done < <(find "$src_dir" -type f -print0)
}

echo "Running shared-infra sync"
echo "- mode: $MODE"
echo "- shared root: $SHARED_ROOT"
echo "- target root: $TARGET_ROOT"

# Core shared directories
sync_tree "$SHARED_ROOT/.agents/skills" "$TARGET_ROOT/.agents/skills"
sync_tree "$SHARED_ROOT/.github/skills" "$TARGET_ROOT/.github/skills"
sync_tree "$SHARED_ROOT/.agent/profiles" "$TARGET_ROOT/.agent/profiles"
copy_persona_if_missing_or_warn "$SHARED_ROOT/.agent/codex.md" "$TARGET_ROOT/.agent/codex.md"

# Baseline setup assets from templates
copy_file "$SHARED_ROOT/templates/AGENTS.md.template" "$TARGET_ROOT/AGENTS.md"
copy_file "$SHARED_ROOT/templates/Makefile.workteam.template" "$TARGET_ROOT/Makefile.workteam"
copy_file "$SHARED_ROOT/templates/.env.example.template" "$TARGET_ROOT/.env.example"
copy_file "$SHARED_ROOT/templates/.devcontainer/devcontainer.json.template" "$TARGET_ROOT/.devcontainer/devcontainer.json"
copy_file "$SHARED_ROOT/templates/.devcontainer/postCreate.sh.template" "$TARGET_ROOT/.devcontainer/postCreate.sh"
copy_file "$SHARED_ROOT/templates/.devcontainer/Dockerfile.template" "$TARGET_ROOT/.devcontainer/Dockerfile"
copy_file "$SHARED_ROOT/templates/.vscode/settings.json.template" "$TARGET_ROOT/.vscode/settings.json"
copy_file "$SHARED_ROOT/templates/.vscode/mcp.json.template" "$TARGET_ROOT/.vscode/mcp.json"

mkdir -p "$TARGET_ROOT/.agent"
shared_ref="$(git -C "$SHARED_ROOT" rev-parse --short HEAD 2>/dev/null || echo unknown)"
cat > "$TARGET_ROOT/.agent/shared-infra.lock" <<EOF
shared_root=$SHARED_ROOT
shared_ref=$shared_ref
synced_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
mode=$MODE
EOF
echo "WRITE: $TARGET_ROOT/.agent/shared-infra.lock"

echo "Done."
