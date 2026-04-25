#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--help" ]]; then
  echo "Usage: scripts/verify_layout.sh"
  echo "Checks required shared-infra directories/files."
  exit 0
fi

required=(
  ".agents/skills"
  ".github/skills"
  ".agent/profiles"
  "templates"
  "templates/.devcontainer"
  "templates/.vscode"
  "docs"
  "scripts"
  "README.md"
  "Dockerfile"
  ".devcontainer/devcontainer.json"
  ".devcontainer/postCreate.sh"
  "docs/skills_and_components_classification.md"
)

missing=0
for p in "${required[@]}"; do
  if [[ ! -e "$p" ]]; then
    echo "Missing: $p"
    missing=1
  fi
done

if [[ $missing -ne 0 ]]; then
  echo "FAIL: shared-infra layout incomplete"
  exit 1
fi

echo "PASS: shared-infra layout complete"
