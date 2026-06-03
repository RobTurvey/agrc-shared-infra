---
name: skills_creator
description: Use this skill when the user asks to create a new agent skill or refactor an existing skill into a modular, cross-agent compatible package.
---

# skills_creator

## Purpose
Create discoverable, reusable, and testable skills with strong activation metadata and a practical iteration loop that works across agent environments.

## Invoke When
- A user asks to create a new skill from requirements.
- A user asks to convert ad-hoc instructions into a formal skill package.
- A user asks to add examples, templates, or scripts for repeatable skill behavior.

## Communicating with users
- Calibrate language to user context; avoid unexplained jargon when user sophistication is unclear.
- Briefly define terms like "assertion", "benchmark", or "schema" when needed.
- Prefer concise, concrete phrasing and confirm assumptions before deep implementation.

## Required Structure
```text
<skill-name>/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

## Workflow
1. Capture intent before drafting:
	- What should this skill enable the agent to do?
	- When should it trigger (phrases/contexts)?
	- What output format is expected?
	- Should test cases be added now?
2. Confirm target location and naming.
3. Write `SKILL.md` frontmatter first with explicit trigger phrasing.
4. Keep core instructions concise; move depth to `references/`.
5. Add deterministic scripts for repeatable tasks.
6. Add templates/examples in `assets/`.
7. Add cross-agent handshake guidance to avoid instruction/skill overlap.
8. Run lightweight validation (self-test prompts) before formal package validation.
9. Run deterministic validation before handoff.

## Discovery Rules
- Description must start with an action phrase.
- Description must include: `Use this skill when ...`.
- Description should include at least two concrete user intent patterns.
- Description should include near-miss contexts to reduce under-triggering.

## Cross-Agent Registration
- Shared location: `.agents/skills/<skill-name>/`.
- Copilot location: `.github/skills/<skill-name>/SKILL.md`.
- Codex and Claude can point to the shared `.agents/skills/` path.
- Keep global path compatibility in mind for user-level skills: `~/.agents/skills/<skill-name>/`.

## Context Hygiene Rules
- Keep broad always-on rules in instruction files, not in skill bodies.
- Keep task-specific workflows and capability procedures in `SKILL.md`.
- Move deep/static detail to `references/` for progressive disclosure.
- Use `assets/` for examples/templates and stable output patterns.

## Progressive Disclosure Guidelines
- Keep `SKILL.md` focused; if it grows large, split detail into named reference files and point to them explicitly.
- Organize references by variant when domain-specific behavior differs (for example provider/framework/cloud).
- Include a short table of contents for long reference files.

## Script Policy
- Use Python for parsing/transformation logic.
- Every script must support `--help`.
- Return non-zero exit code on failure.

## Evaluation and iteration (capability-based)
Use a right-sized loop based on available tooling:

1. Draft 2-3 realistic test prompts with expected outcomes.
2. If environment supports parallel agents/baseline comparison:
	- Run with-skill and baseline in parallel.
	- Capture timing/cost/quality signals where available.
3. If parallel/baseline tooling is unavailable:
	- Run serial qualitative checks and collect explicit user feedback.
4. Improve the skill using feedback:
	- generalize beyond single examples,
	- keep prompt/instructions lean,
	- explain "why" for important constraints,
	- bundle repeated helper logic into `scripts/`.
5. Repeat until quality is stable or user confirms completion.

## Trigger-description optimization (optional)
- For high-value skills, create should-trigger and should-not-trigger query sets.
- Prefer realistic, nuanced near-miss negatives over obviously irrelevant negatives.
- If trigger-eval tooling exists in the environment, use it; otherwise perform manual review and refine description iteratively.

## Validation Gate
- Validate package structure and activation phrasing with:
	- `python3 .agents/skills/qa_skills/scripts/validate_skill_package.py --path .agents/skills/<skill-name>`
- Ensure folder name matches frontmatter `name`.
- Ensure at least one concrete blueprint/example exists in `assets/`.

## Toolkit Files
- Script scaffold helper: `scripts/create_skill.py`
- Frontmatter template: `assets/skill_frontmatter_template.md`
- Package checklist: `assets/skill_package_checklist.md`
- Naming and activation guide: `references/naming_and_activation.md`
- Q&A source of truth: `references/skills_create.md`
- Q&A implementation summary: `references/skills_creat_summary.md`
- Gold-standard blueprint: `assets/blueprint_analyze_logs/`
