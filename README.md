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
