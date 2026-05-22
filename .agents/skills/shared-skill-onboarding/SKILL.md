---
name: shared-skill-onboarding
description: Use this skill when the user asks to import, review, register, or publish a new shared skill package into shared-infra with canonical and Copilot discovery paths.
---

# shared-skill-onboarding

## Purpose

Provide a deterministic workflow for onboarding new skills into shared-infra so distribution to downstream projects stays consistent.

## Invoke When

- The user asks to add a new skill package into this repository.
- The user asks if a skill is suitable for shared-infra.
- The user asks to wire a skill into expected format and docs.

## Required Inputs

- Source skill package location (zip path or folder path)
- Skill name (or inferred folder name)
- Optional issue ID for tracking

## Guardrails

- Keep only generic, reusable skills in shared-infra.
- Do not import project-specific business workflows.
- Do not execute untrusted scripts from imported packages during review.

## Workflow

1. Read and review source package contents.
2. Validate reusable scope using the shared-vs-project rules.
3. Install canonical package in `.agents/skills/<skill-name>/`.
4. Add Copilot entrypoint in `.github/skills/<skill-name>/SKILL.md`.
5. Register skill in `docs/skills_and_components_classification.md`.
6. Update `README.md` discoverability note if broadly relevant.
7. Run repository checks and report status.
8. Commit and push when requested.

## Required Reference

- `docs/skill_onboarding_process.md`

## Validation Commands

- `make -f Makefile.shared verify-layout`
- `make -f Makefile.shared verify-skill`
- `make -f Makefile.shared verify-templates`
