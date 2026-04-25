# skills_creator implementation summary

This document is the build-spec for creating or refactoring skills in a multi-agent environment (Copilot, Roo, Claude Code). It captures only implementation-critical guidance.

## Objective
- Produce reusable, discoverable skills with minimal context overhead.
- Keep skill behavior deterministic and validation-driven.
- Ensure cross-agent compatibility without relying on fragile symlink behavior.

## Canonical locations
- Primary repository path: `.agents/skills/<skill-name>/`.
- Optional user-global path: `~/.agents/skills/<skill-name>/`.
- Copilot entrypoint mirror: `.github/skills/<skill-name>/SKILL.md` (kept concise and synced to canonical).

## Required package structure
```text
<skill-name>/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

## Context hygiene contract
- Put always-on/global rules in instruction files (not in skills).
- Put task workflow/capability logic in `SKILL.md`.
- Put deep/static material in `references/`.
- Put templates/examples/blueprints in `assets/`.
- Put deterministic executable logic in `scripts/`.

## SKILL.md authoring standard
1. Frontmatter must include `name` and `description`.
2. `description` must begin with `Use this skill when...`.
3. Description must include at least two concrete trigger intents.
4. Body must be concise, procedural, and output-oriented.
5. Heavy detail should be deferred to `references/`.

## Script policy
- Prefer Python for parsing/transformation logic.
- Every script must support `--help`.
- Scripts must return non-zero exit codes on failure.
- Scripts should be deterministic and avoid hidden side effects.

## Creation workflow (meta-skill behavior)
1. Confirm skill name, scope, and target path.
2. Scaffold package structure.
3. Draft `SKILL.md` first (activation metadata + concise procedure).
4. Add `references/` only for deep context required at runtime.
5. Add `assets/` for reusable templates and a gold-standard example when relevant.
6. Add `scripts/` only when deterministic automation adds value.
7. Validate package, then record evidence in issue notes.

## Quality gates (must pass)
1. Folder name matches frontmatter `name` exactly.
2. Activation phrase format is correct and specific.
3. Required directories/files are present.
4. If scripts exist, `--help` and failure behavior are correct.
5. At least one blueprint/template exists in `assets/` for non-trivial skills.
6. Validator evidence is captured before handoff.

## Validation command
`python3 .agents/skills/qa_skills/scripts/validate_skill_package.py --path .agents/skills/<skill-name>`

## Gold-standard blueprint reference
- Use `.agents/skills/skills_creator/assets/blueprint_analyze_logs/` as the canonical example of progressive disclosure:
  - concise `SKILL.md`
  - deterministic script usage
  - deep context in `references/`
  - output template in `assets/`

## Done definition for skills_creator output
- The generated skill is discoverable, concise, and deterministic.
- The package passes validator checks.
- Cross-agent pathing and handoff notes are complete.

