#!/usr/bin/env bash
set -euo pipefail

echo "[postCreate] shared-infra bootstrap starting..."

if [ -f package.json ]; then
  echo "[postCreate] Installing npm dependencies..."
  npm install
else
  echo "[postCreate] No package.json found, skipping npm install."
fi

echo "[postCreate] Checking core prerequisites..."
command -v git >/dev/null || echo "Missing: git"
command -v go >/dev/null || echo "Missing: go"
command -v make >/dev/null || echo "Missing: make"
command -v jq >/dev/null || echo "Missing: jq"
command -v dolt >/dev/null || echo "Missing: dolt"
command -v aws >/dev/null || echo "Missing: aws"
command -v npm >/dev/null || echo "Missing: npm"

if command -v aws >/dev/null 2>&1; then
  echo "[postCreate] aws cli: $(aws --version 2>&1)"
  if aws sts get-caller-identity --output json >/dev/null 2>&1; then
    echo "[postCreate] AWS credentials available in container."
  else
    echo "[postCreate] AWS credentials not yet available (run aws configure or set AWS_PROFILE)."
  fi
fi

if command -v bd >/dev/null 2>&1; then
  echo "[postCreate] bd already available: $(command -v bd)"
else
  echo "[postCreate] bd CLI not found."
  if [ -n "${BD_INSTALL_CMD:-}" ]; then
    echo "[postCreate] Attempting BD_INSTALL_CMD install..."
    bash -lc "$BD_INSTALL_CMD" || true
  else
    echo "[postCreate] Attempting install from gastownhall/beads..."
    curl -fsSL https://raw.githubusercontent.com/gastownhall/beads/main/scripts/install.sh | bash || true
  fi

  if ! command -v bd >/dev/null 2>&1; then
    echo "[postCreate] Falling back to npm global install (@beads/bd)..."
    npm install -g @beads/bd || true
  fi
fi

if command -v bd >/dev/null 2>&1; then
  echo "[postCreate] bd installed: $(command -v bd)"
else
  echo "[postCreate] WARNING: bd still unavailable."
  echo "[postCreate] Set BD_INSTALL_CMD and rerun: bash .devcontainer/postCreate.sh"
fi
