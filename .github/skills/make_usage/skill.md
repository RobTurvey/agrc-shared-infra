---
name: make_usage
description: Use this skill when the user asks to execute or choose Make targets for runtime checks initialization QA and closeout workflows.
---

# make_usage (Copilot entrypoint)

Canonical implementation: [`.agents/skills/make_usage/SKILL.md`](.agents/skills/make_usage/SKILL.md:1)

## Behavior
1. Map user request to the correct Make target.
2. Validate required variables (`ISSUE`, `ACTOR`, `NOTE`).
3. Prefer project Make workflows over ad-hoc manual steps.

## Toolkit
- [`.agents/skills/make_usage/references/make_targets.md`](.agents/skills/make_usage/references/make_targets.md:1)
- [`.agents/skills/make_usage/assets/make_run_checklist.md`](.agents/skills/make_usage/assets/make_run_checklist.md:1)
- [`.agents/skills/make_usage/scripts/suggest_make_command.py`](.agents/skills/make_usage/scripts/suggest_make_command.py:1)

