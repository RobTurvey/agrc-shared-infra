---
name: skills_creator
description: Use this skill when the user asks to create a new skill package or refactor instructions into a reusable SKILL-based workflow.
---

# skills_creator (Copilot entrypoint)

Use the shared implementation in [`../../../.agents/skills/skills_creator/SKILL.md`](../../../.agents/skills/skills_creator/SKILL.md) as the canonical source.

## Behavior
1. Interpret user request for skill creation/refactor.
2. Capture intent before drafting (trigger context, output shape, and test expectation).
2. Build package using `SKILL.md`, `scripts/`, `references/`, `assets/`.
3. Ensure metadata starts with clear activation phrase: `Use this skill when ...`.
4. Keep body concise and push detailed context to `references/`.
5. Keep always-on rules in instruction files, not in skill bodies.
6. Use capability-based evaluation loops (parallel baseline when available, serial qualitative fallback otherwise).
7. Run deterministic package validation before handoff.

## Shared Toolkit
- [`../../../.agents/skills/skills_creator/scripts/create_skill.py`](../../../.agents/skills/skills_creator/scripts/create_skill.py)
- [`../../../.agents/skills/skills_creator/assets/skill_frontmatter_template.md`](../../../.agents/skills/skills_creator/assets/skill_frontmatter_template.md)
- [`../../../.agents/skills/skills_creator/assets/skill_package_checklist.md`](../../../.agents/skills/skills_creator/assets/skill_package_checklist.md)
- [`../../../.agents/skills/skills_creator/references/skills_creat_summary.md`](../../../.agents/skills/skills_creator/references/skills_creat_summary.md)

