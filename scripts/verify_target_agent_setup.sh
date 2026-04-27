#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  echo "Usage: scripts/verify_target_agent_setup.sh --target-root <path>"
  exit 0
fi

TARGET_ROOT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --target-root)
      TARGET_ROOT="${2:-}"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$TARGET_ROOT" ]]; then
  echo "Usage: scripts/verify_target_agent_setup.sh --target-root <path>"
  exit 1
fi

TARGET_ROOT="$(cd "$TARGET_ROOT" && pwd)"

required=(
  "AGENTS.md"
  "Makefile.workteam"
  ".agent/profiles"
  ".agents/skills"
  ".github/skills"
  ".devcontainer/devcontainer.json"
  ".devcontainer/Dockerfile"
  ".devcontainer/postCreate.sh"
  ".agent/shared-infra.lock"
)

missing=0
for rel in "${required[@]}"; do
  if [[ ! -e "$TARGET_ROOT/$rel" ]]; then
    echo "Missing: $rel"
    missing=1
  fi
done

if [[ $missing -ne 0 ]]; then
  echo "FAIL: target repository is not agent-ready"
  exit 1
fi

echo "PASS: target repository has required agent setup baseline"
