# agrc-shared-infra

Shared AGRC agent infrastructure templates and reusable workflow assets.

## Purpose

This repository contains shared, reusable assets that are consumed by AGRC repositories
to keep agent workflows consistent across projects.

## Baseline Contents

- `.agents/skills/` canonical skill implementations.
- `.github/skills/` Copilot entrypoints for skill discovery.
- `.agent/profiles/` runtime profile references.
- `templates/` starter templates for new repositories.
- `scripts/` validation and bootstrap scripts.
- `docs/` shared-vs-project classification and governance docs.
- `Makefile.shared` common verification targets.

## Infra-Only Positioning

This repository is intended to stay focused on **infrastructure and workflow baseline assets**
that are reusable across AGRC repositories.

- Keep here: runtime profiles, automation templates, QA/process skills, reusable command wrappers,
  devcontainer/IDE scaffolding, MCP integration templates and policy docs.
- Keep in project repos: business-domain skills, project-specific deployment/playbooks,
  app-specific debug configs, and repository-local runbooks.

See:
- `docs/agent_setup_spec.md`
- `docs/skills_and_components_classification.md`
- `docs/beads_troubleshooting.md`

## Shared-Infra Devcontainer (Runnable)

This repo now includes a runnable devcontainer baseline:

- `.devcontainer/devcontainer.json`
- `.devcontainer/postCreate.sh`
- `Dockerfile`

Beads installation path is pinned to:

`https://raw.githubusercontent.com/gastownhall/beads/main/scripts/install.sh`

The URL is used in both image build and post-create fallback install flow.

### Open in Container

1. Open this repository root in VS Code.
2. Run **Dev Containers: Reopen in Container**.
3. Post-create checks install/verify baseline tools (`bd`, `dolt`, `aws`, `make`, `jq`, `go`).

## Consumption Patterns

### Option 1: Git submodule (recommended)

```bash
git submodule add -b main https://github.com/RobTurvey/agrc-shared-infra.git shared-infra
```

Then reference shared content from your target repository.

### Option 2: Sync copy (fallback)

Copy required files from this repo into your project if submodules are not allowed.
Track source commit hash in your repo notes for traceability.

### One-command target repo bootstrap and refresh

Use the shared make targets to install/update common agent setup in a target repository:

```bash
# First-time setup (non-destructive; creates missing baseline files)
make -f Makefile.shared target-bootstrap TARGET_ROOT=/path/to/target-repo

# Ongoing updates (sync shared-managed assets; backups written for changed files)
make -f Makefile.shared target-refresh TARGET_ROOT=/path/to/target-repo

# Verify required agent baseline exists in target repository
make -f Makefile.shared verify-target-agent-setup TARGET_ROOT=/path/to/target-repo
```

Notes:
- Bootstrap does not overwrite existing files in target repos.
- Refresh updates shared-managed files and writes `*.shared-infra.bak.<timestamp>` backups before replacement.
- A sync lock file is written to `.agent/shared-infra.lock` in the target repo.

#### If target repo does not have `Makefile.shared` yet

Run from inside the target repo and point `make` at a temporary clone of shared-infra:

```bash
git clone --depth 1 https://github.com/RobTurvey/agrc-shared-infra.git /tmp/agrc-shared-infra
make -f /tmp/agrc-shared-infra/Makefile.shared target-bootstrap TARGET_ROOT="$(pwd)" SHARED_ROOT=/tmp/agrc-shared-infra
make -f /tmp/agrc-shared-infra/Makefile.shared verify-target-agent-setup TARGET_ROOT="$(pwd)"
```

### Pre-devcontainer bootstrap (critical first-time flow)

When a target repo has no agent/devcontainer setup yet, run these **before** trying to build or reopen in container:

1. Clone shared-infra locally.
2. Run [`target-bootstrap`](Makefile.shared:27) against the target repo.
3. Run [`verify-target-agent-setup`](Makefile.shared:35).
4. Confirm these files now exist in the target repo:
   - [`.devcontainer/devcontainer.json`](templates/.devcontainer/devcontainer.json.template:1)
   - [`.devcontainer/Dockerfile`](templates/.devcontainer/Dockerfile.template:1)
   - [`.devcontainer/postCreate.sh`](templates/.devcontainer/postCreate.sh.template:1)

After those files are present, open the target repo in VS Code and run **Dev Containers: Reopen in Container**.

Post-container first session:
- Run runtime initialization from the target repo `Makefile.workteam`:
  - `make agent-runtime-resolve`
  - `make agent-init ISSUE=<id> ACTOR=<agrc/copilot|agrc/roo|agrc/claude>`
- If Beads UI is needed, start it from a repo that has [`beads-ui-up`](Makefile.shared:256) available (for example shared-infra) or via `npx beads-ui` in the target container.

Later refresh (same pattern):

```bash
make -f /tmp/agrc-shared-infra/Makefile.shared target-refresh TARGET_ROOT="$(pwd)" SHARED_ROOT=/tmp/agrc-shared-infra
make -f /tmp/agrc-shared-infra/Makefile.shared verify-target-agent-setup TARGET_ROOT="$(pwd)"
```

## Verification

Run both checks before tagging a release:

```bash
make -f Makefile.shared verify-layout
make -f Makefile.shared verify-skill
```

Optional:

```bash
make -f Makefile.shared show-classification
```

## Versioning Policy

- Use semantic-style baseline tags for shared snapshots.
- First baseline: `v0.1.0`.
- Increment patch for docs/tooling fixes (`v0.1.1`).
- Increment minor for new templates/skills (`v0.2.0`).

## Release Steps

```bash
git add .
git commit -m "chore: baseline shared infra v0.1.0"
git push
git tag v0.1.0
git push origin v0.1.0
```
