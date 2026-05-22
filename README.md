# agrc-shared-infra

Shared AGRC agent infrastructure templates and reusable workflow assets.

## Purpose

This repository contains shared, reusable assets that are consumed by AGRC repositories
to keep agent workflows consistent across projects.

## Baseline Contents

- `.agents/skills/` canonical skill implementations.
- Includes reusable brand/design and motion handoff skills such as `brand-guidelines-builder` and `promo-video`.
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
- `docs/skill_onboarding_process.md`
- `docs/beads_troubleshooting.md`

## Shared-Infra Devcontainer (Runnable)

This repo now includes a runnable devcontainer baseline:

- `.devcontainer/devcontainer.json`
- `.devcontainer/postCreate.sh`
- `Dockerfile` (for this shared-infra repository itself)

For target repositories bootstrapped from shared-infra, the container build file is:

- `.devcontainer/Dockerfile` (provisioned from [`templates/.devcontainer/Dockerfile.template`](templates/.devcontainer/Dockerfile.template:1))

The target `.devcontainer/Dockerfile` baseline includes:
- Node.js 22 (via `mcr.microsoft.com/devcontainers/javascript-node:1-22-bookworm`)
- Python 3 (`python3`, `python3-pip`, `python3-venv`)

Beads installation path is pinned to:

`https://raw.githubusercontent.com/gastownhall/beads/main/scripts/install.sh`

The URL is used in both image build and post-create fallback install flow.

### Open in Container

1. Open this repository root in VS Code.
2. Run **Dev Containers: Reopen in Container**.
3. Post-create checks install/verify baseline tools (`bd`, `dolt`, `aws`, `make`, `jq`, `go`).

## Consumption Patterns

### Required order for new/existing target repos (no submodule flow)

Use sync-based bootstrap/refresh only. The order below is mandatory.

#### 1) Pre-devcontainer bootstrap (must happen first)

When a target repo has no agent/devcontainer setup yet, run these **before** trying to build or reopen in container.

If target repo does not have `Makefile.shared`, run from inside the target repo and point `make` at a temporary clone of shared-infra:

```bash
git clone --depth 1 https://github.com/RobTurvey/agrc-shared-infra.git /tmp/agrc-shared-infra
make -f /tmp/agrc-shared-infra/Makefile.shared target-bootstrap TARGET_ROOT="$(pwd)" SHARED_ROOT=/tmp/agrc-shared-infra
make -f /tmp/agrc-shared-infra/Makefile.shared verify-target-agent-setup TARGET_ROOT="$(pwd)"
```

Confirm these files now exist in the target repo:
   - [`.devcontainer/devcontainer.json`](templates/.devcontainer/devcontainer.json.template:1)
   - [`.devcontainer/Dockerfile`](templates/.devcontainer/Dockerfile.template:1)
   - [`.devcontainer/postCreate.sh`](templates/.devcontainer/postCreate.sh.template:1)

Notes:
- Bootstrap does not overwrite existing files in target repos.
- A sync lock file is written to `.agent/shared-infra.lock` in the target repo.

#### 2) Rebuild/open container (after pre-devcontainer bootstrap)

After step 1 is complete, open the target repo in VS Code and run:

- **Dev Containers: Rebuild and Reopen in Container**

#### 3) Test and validate setup in the container

Inside the target repo container:

- Run runtime initialization from [`Makefile.workteam`](templates/Makefile.workteam.template:1):
  - `make agent-runtime-resolve`
  - `make agent-init ISSUE=<id> ACTOR=<agrc/copilot|agrc/roo|agrc/claude>`
- Validate baseline files are in place (already covered by [`verify-target-agent-setup`](Makefile.shared:36)).
- If Beads UI is needed, start it from a repo that has [`beads-ui-up`](Makefile.shared:256) available (for example shared-infra) or run `npx -y beads-ui@latest start --port 3002` in the target container.

#### 4) Ongoing refresh (after initial setup)

Run refresh whenever new shared skills/plugins are published:

```bash
make -f /tmp/agrc-shared-infra/Makefile.shared target-refresh TARGET_ROOT="$(pwd)" SHARED_ROOT=/tmp/agrc-shared-infra
make -f /tmp/agrc-shared-infra/Makefile.shared verify-target-agent-setup TARGET_ROOT="$(pwd)"
```

Refresh updates shared-managed assets and writes `*.shared-infra.bak.<timestamp>` backups before replacement.

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
