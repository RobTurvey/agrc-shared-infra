# Beads Troubleshooting (shared-infra)

This runbook covers common Beads setup/runtime issues inside the shared-infra devcontainer.

## Quick Checks

Run inside container:

```bash
command -v bd
command -v dolt
bd --help
make -f Makefile.shared verify-layout
```

## Common Problems

### 1) `bd` not found

Symptoms:
- `command -v bd` returns nothing

Fix:
```bash
curl -fsSL https://raw.githubusercontent.com/gastownhall/beads/main/scripts/install.sh | bash
command -v bd || npm install -g @beads/bd
command -v bd
```

Notes:
- The devcontainer uses `BD_INSTALL_CMD` with the same URL in
  `.devcontainer/devcontainer.json`.

### 2) Beads install script fails in postCreate

Symptoms:
- Post-create logs show install failure

Fix:
```bash
bash .devcontainer/postCreate.sh
```

If still failing, run fallback:
```bash
npm install -g @beads/bd
```

### 3) `dolt` not found

Symptoms:
- `command -v dolt` missing

Fix:
```bash
curl -L https://github.com/dolthub/dolt/releases/latest/download/install.sh | bash
command -v dolt
```

If persistent, rebuild container so Dockerfile provisioning re-runs.

### 4) Permissions warning on `.beads`

Symptoms:
- Warning: `.beads has permissions 0777 (recommended: 0700)`

Fix:
```bash
chmod 700 .beads
```

### 5) AWS CLI present but credentials unavailable

Symptoms:
- `aws sts get-caller-identity` fails

Fix:
- Ensure host has credentials in `~/.aws`
- Reopen devcontainer (mount configured in `.devcontainer/devcontainer.json`)
- Or configure credentials/profile inside container.

### 6) Make targets fail from wrong directory

Symptoms:
- `./scripts/verify_layout.sh: No such file or directory`

Fix:
```bash
cd shared-infra
make -f Makefile.shared verify-layout
```

## Validation Sequence

Use this after fixing any issue:

```bash
cd shared-infra
make -f Makefile.shared verify-layout
make -f Makefile.shared verify-skill
make -f Makefile.shared verify-templates
```

Expected: all PASS.
