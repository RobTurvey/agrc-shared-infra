# Agent Setup Specification (shared-infra)

## Purpose

Define a reusable, project-agnostic specification so a new repository can connect to `shared-infra` and get a consistent AGRC agent runtime from day one.

This spec separates:
- **Common baseline** (owned by `shared-infra`)
- **Project overlays** (owned by each target repository)

## Design Goals

1. New repos should bootstrap quickly with minimal manual setup.
2. Agent behavior should be consistent across repos.
3. Shared controls (runtime, Beads workflow, security guardrails, templates) should be versioned centrally.
4. Project-specific business logic should stay local.

## Scope of Shared Baseline

The following are expected to be common and sourced from `shared-infra`:

1. Agent policy/profile baseline
   - `.agent/profiles/container-beads.md`
   - `.agent/profiles/local-lite.md`

2. Shared skill library and entrypoints
   - `.agents/skills/*` (canonical)
   - `.github/skills/*` (entrypoints)

3. Shared runtime scaffolding
   - `.devcontainer/devcontainer.json`
   - `.devcontainer/postCreate.sh`
   - `Dockerfile`

4. Shared templates for greenfield repos
   - `templates/AGENTS.md.template`
   - `templates/Makefile.workteam.template`
   - `templates/.env.example.template`
   - `templates/.devcontainer/*`
   - `templates/.vscode/*`

5. Shared operational docs
   - Skills/component classification
   - Beads troubleshooting

## Project-Specific Overlay (Do Not Centralize)

Each target repository keeps local ownership of:

1. Domain-specific skills/runbooks
   - Product/business workflows
   - App-specific deployment or incident details

2. Project Make targets
   - Build/test/deploy commands tied to local stack

3. Project debug profiles
   - `.vscode/launch.json` entries tied to local scripts

4. Secret/env details
   - Any real credentials, account IDs, private endpoints

## Integration Modes

### Mode A (recommended): Git submodule

Use `shared-infra` as a pinned dependency and selectively wire paths into the host repo.

Benefits:
- Explicit version pinning
- Controlled updates
- Traceable change history

### Mode B: Sync copy

Copy files from `shared-infra` into the target repo and track source version manually.

Benefits:
- Simpler for repos that cannot use submodules
- Easier for teams that want local-only ownership

Tradeoff:
- Manual drift management

## Required Bootstrap Contract for New Repos

A new repo is considered "agent-ready" when all are true:

1. Runtime detection and init commands are available and documented.
2. Devcontainer opens and post-create setup completes.
3. Beads CLI is available in container runtime.
4. Shared skill paths resolve (canonical + entrypoints).
5. Make-based verification passes.
6. Secret-handling and tracking guardrails are present.

## Minimal File Contract (Target Repo)

At minimum, target repo should contain (directly or via wiring):

1. `AGENTS.md`
2. `Makefile.workteam`
3. `.agent/profiles/*`
4. `.agents/skills/*` (shared + local)
5. `.github/skills/*`
6. `.devcontainer/devcontainer.json`
7. `.devcontainer/postCreate.sh`

## Runtime Behavior Contract

1. `container-beads`
   - `bd` required for tracking
   - Beads workflow is system of record

2. `local-lite`
   - No direct `bd` execution
   - Local work is synced back to Beads from container runtime

## Validation Contract

For shared baseline verification:

```bash
cd shared-infra
make -f Makefile.shared verify-layout
make -f Makefile.shared verify-skill
make -f Makefile.shared verify-templates
```

For target repo adoption, define project-local acceptance checks that include:
- runtime resolve
- agent init
- QA check target
- Beads note/checklist flow

## Versioning and Rollout

1. Tag `shared-infra` releases (semver style).
2. Projects pin a tested release/tag.
3. Upgrade flow:
   - pull new shared version
   - run local acceptance checks
   - document deltas and overrides

## Governance Rules

1. Shared changes must remain generic and reusable.
2. Project-specific logic must not be forced into shared baseline.
3. If a shared component breaks one project, local overlay may patch temporarily; durable fix should return to shared baseline.

## Current Decision Snapshot (from owner)

Shared in `shared-infra`:
- frontend/design stack
- website review stack
- web3 testing
- beads_jira_sync (shared target; currently not operational)

Project-local:
- AGRC domain/auction/wallet-specific workflows and implementation runbooks.

