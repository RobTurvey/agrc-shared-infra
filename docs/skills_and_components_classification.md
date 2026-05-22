# Shared vs Project-Specific Classification (Skills, MCP, and Tooling)

This document defines what belongs in `agrc-shared-infra` versus what stays in a project repository.

## Decision Rules

A component is **shared** when all of the following are true:
- It is not tied to one business domain, contract, or service topology.
- It can be reused in 2+ repositories without content changes.
- It improves agent/runtime consistency (workflow, quality, automation, environment parity).

A component is **project-specific** when any of the following is true:
- It encodes domain playbooks (for example AGRC auction lifecycle specifics).
- It requires project-only infra naming, service IDs, schemas, or runbook assumptions.
- It exists only to support one application/runtime implementation.

## Skills Classification (Current Repo Inventory)

### Candidate Shared Skills (move/keep in shared-infra)
- `beads_usage`
- `make_usage`
- `qa_skills`
- `qa_task_review`
- `skills_creator`
- `skill_harvest`
- `shared-skill-onboarding`
- `support_incident`
- `frontend-design`
- `brand-guidelines-builder`
- `promo-video`
- `website-review`
- `website_review` *(duplicate naming variant; consolidate to one canonical package)*
- `ckm-brand`, `ckm-design`, `ckm-design-system`, `ckm-ui-styling`, `ui-ux-pro-max`
- `web3-testing`
- `beads_jira_sync` *(shared target; currently not operational and needs remediation in shared baseline)*

### Project-Specific Skills (keep in project repos)
- `agrc_wallet`
- `aws-ecs-monitor`
- `auction-happy-path-validation`
- `opensea-offer-checker`
- `reporting_validation`
- `prod_deployment`
- `aws-deployments` *(can be split: generic deploy guardrails shared; AGRC deployment wiring local)*
- `website_migration_execution` *(migration of specific website/app context)*

## MCP / Tooling Classification

### Shared candidates
- `.vscode/settings.json` baseline editor/search exclusions and formatting defaults.
- `.vscode/mcp.json` template with placeholder servers and disabled-by-default examples.
- `.devcontainer/devcontainer.json` baseline with neutral extensions and post-create hook.
- `.devcontainer/postCreate.sh` baseline bootstrap script with safe checks and placeholders.
- `roo.yaml` template for multi-agent orchestration baseline.

### Project-local components
- Debug launch configurations targeting project scripts (`.vscode/launch.json` entries that run project-specific files).
- MCP server configs that embed project endpoints, credentials names, or domain-specific command args.
- Any script requiring project-specific folder structure or services.

## Proposed Split Plan

1. Keep `shared-infra` as canonical source of generic templates + governance docs.
2. Export only generic skills into `shared-infra/.agents/skills/*` and mirrored `.github/skills/*` entrypoints.
3. In each project repo, keep domain skills under local `.agents/skills` and add README pointers to shared source.
4. Add compatibility layer in project repos:
   - `AGENTS.md` references both shared and local skill paths.
   - Local overrides are allowed only when explicitly documented.
5. Version shared infra with semver tags and changelog notes for downstream pinning.

## Owner Decisions (Applied)

1. `frontend-design` and website review/design stack: **Shared infra**.
2. `web3-testing`: **Shared infra**.
3. `beads_jira_sync`: **Shared infra** (known not working currently; keep shared with explicit remediation work).

## Current Recommendation (Applied Baseline)

- Move/maintain generic process and quality skills in `shared-infra`.
- Keep shared skill intake and registration workflow in `shared-infra` (`shared-skill-onboarding`) to ensure deterministic skill onboarding.
- Keep brand/design-system extraction skills (including `brand-guidelines-builder`) in `shared-infra` because they are reusable across domains.
- Keep generic motion-content generation skills (including `promo-video`) in `shared-infra` because they are reusable across brands and products.
- Keep AGRC auction and wallet operational skills in project repos.
- Keep MCP templates shared; keep concrete MCP instances project-local.
