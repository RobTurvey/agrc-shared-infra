---
name: shared_infra_bootstrap
description: Use this skill when setting up or hardening agrc-shared-infra for multi-repo reuse, including baseline folder skeleton, versioning, and consumption patterns for website and auction repositories.
---

# shared_infra_bootstrap

## Purpose
Create and maintain a stable shared-infrastructure repository that can be consumed by AGRC repos (for example AGENTREALCOIN2 and auction) without duplicating agent workflow assets.

## Invoke When
- User asks to initialize or populate shared-infra repository content.
- User asks to standardize reusable agent assets across multiple AGRC repos.
- User asks to prepare shared-infra for submodule-based consumption.

## Do Not Invoke When
- Work is only inside one repo and no shared assets are required.
- User asks for feature implementation unrelated to repo bootstrap/governance.

## Inputs Expected
- Target repository URL for shared-infra.
- Source repository path(s) for canonical assets to copy or adapt.
- Consumption mode: `git submodule` or `sync copy`.
- Initial version tag (default: `v0.1.0`).

## Required Structure
- `.agents/skills/` canonical skill implementations.
- `.github/skills/` Copilot entrypoints redirecting to canonical skills.
- `.agent/profiles/` shared runtime profiles.
- `templates/` for reusable repo bootstrap templates.
- `scripts/` for deterministic bootstrap checks.

## Workflow
1. Confirm shared-infra repository is reachable and has at least one commit.
2. Create baseline directory skeleton from `references/minimum_layout.md`.
3. Add core documentation: `README.md` and `templates/README.md`.
4. Add at least one shared skill package and matching Copilot entrypoint.
5. Add bootstrap verification script from `scripts/check_shared_infra_ready.py`.
6. Validate structure and summarize gaps.
7. Record Beads milestone comment with what was included and next actions.
8. Tag baseline release (`v0.1.0`) after structure checks pass.

## Output Contract
Provide:
- Created/updated file list.
- Verification output from readiness script.
- Explicit statement of whether repo is ready for submodule consumption.
- Next actions if not fully ready.

## Validation Gate
Pass only when all are true:
- Required directories exist.
- At least one canonical skill and one Copilot entrypoint exist.
- Readiness script exits 0.
- Baseline release plan is documented.

## Toolkit
- Layout reference: `references/minimum_layout.md`
- Checklist template: `assets/bootstrap_checklist.md`
- Readiness script: `scripts/check_shared_infra_ready.py`
