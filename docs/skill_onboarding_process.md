# Skill Onboarding Process (shared-infra)

## Purpose

This document is the standard process for adding a new skill package to shared-infra so it can be reused across projects.

## Scope

Use this process when:
- importing an external skill package from zip, repo, or file share
- promoting an internal skill to shared-infra distribution
- updating an existing shared skill with new assets or references

Do not use this process for project-only business workflow skills.

## Required Output

Every onboarded skill must include:
- Canonical package in `.agents/skills/<skill-name>/`
- Copilot entrypoint in `.github/skills/<skill-name>/SKILL.md`
- Classification registration in `docs/skills_and_components_classification.md`
- Discoverability note in `README.md` when the skill is broadly useful

## Intake Checklist

1. Validate source package format
- Confirm archive or folder is readable and complete.
- Confirm `SKILL.md` exists.
- Confirm no executable or untrusted runtime step is required just to import docs.

2. Validate skill suitability for shared-infra
- Must be generic across multiple projects.
- Must not encode project-only IDs, service topology, private endpoints, or domain runbooks.
- Must be reusable with minimal adaptation.

3. Validate package structure
- Expected minimum: `SKILL.md`
- Preferred: `references/`, `assets/`, and optional `scripts/`

## Import Steps

1. Extract/copy to canonical path
- Place full skill folder at `.agents/skills/<skill-name>/`.

2. Create Copilot entrypoint
- Add `.github/skills/<skill-name>/SKILL.md` with frontmatter:
  - `name: <skill-name>`
  - short actionable `description`
- Include canonical pointer to `.agents/skills/<skill-name>/SKILL.md`.

3. Register in documentation
- Add the skill to candidate shared skills in `docs/skills_and_components_classification.md`.
- Add a short recommendation note when needed.
- Add README mention if this is a commonly used workflow.

4. Verify
- `make -f Makefile.shared verify-layout`
- `make -f Makefile.shared verify-skill`
- `make -f Makefile.shared verify-templates`

5. Commit and publish
- Commit only onboarding-related files.
- Push to remote branch.

## Naming and Conventions

- Use kebab-case for skill folder names.
- For new Copilot entrypoints, use `SKILL.md`.
- Existing lowercase `skill.md` files are legacy and can remain until a separate normalization pass.

## Review Rubric

A skill is ready when:
- discovery path pairing exists (canonical plus entrypoint)
- description clearly states trigger conditions
- instructions are deterministic and practical
- no project-specific business logic leaked into shared baseline

## Example Path Map

For skill name `promo-video`:
- `.agents/skills/promo-video/SKILL.md`
- `.github/skills/promo-video/SKILL.md`
