---
name: beads_usage
description: Use this skill when the user asks to work with bd beads workflows including ready work claiming updates discovered-from links and closure notes.
---

# beads_usage (Copilot entrypoint)

Canonical implementation is in [`.agents/skills/beads_usage/SKILL.md`](.agents/skills/beads_usage/SKILL.md:1).

## Behavior
1. Use `bd` as system of record for issue tracking.
2. Prefer `bd ... --json` commands.
3. Enforce discovered-work linking via `--deps discovered-from:<parent-id>`.
4. Enforce comments for chronological event logging (who/what/when).
5. Enforce mandatory epic/task note checklist before closure.

## Toolkit
- [`.agents/skills/beads_usage/references/beads_commands.md`](.agents/skills/beads_usage/references/beads_commands.md:1)
- [`.agents/skills/beads_usage/assets/beads_task_checklist.md`](.agents/skills/beads_usage/assets/beads_task_checklist.md:1)
- [`.agents/skills/beads_usage/scripts/generate_note_template.py`](.agents/skills/beads_usage/scripts/generate_note_template.py:1)

