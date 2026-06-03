---
name: make_usage
description: Use this skill when the user asks to run project automation via make targets including runtime checks agent initialization QA gates and Beads workflow orchestration.
---

# make_usage

## Purpose
Provide consistent, safe execution of repository Make targets as the primary automation interface.

## Invoke When
- User asks how to run a workflow step with Make.
- User asks for runtime preflight and agent initialization.
- User asks to run QA or handoff checklists.
- User asks for Beads operations via `make` wrappers.

## Core Rules
- Prefer `make <target>` over ad-hoc manual command sequences.
- Validate required params (for example `ISSUE=<id>`, `NOTE=...`) before running target.
- Respect runtime mode: `AGENT_RUNTIME=container-beads` vs `AGENT_RUNTIME=local-lite`.
- Use `agent-runtime-check` and `agent-init` for consistent session bootstrap.

## Standard Workflow
1. Inspect goal and choose a Make target.
2. Run runtime check: `make agent-runtime-check`.
3. Run task init: `make agent-init ISSUE=<id> ACTOR=<agrc/copilot|agrc/codex|agrc/claude>`.
4. Execute operational target (`agent-qa-check`, `agent-comment-checklist`, etc.).
5. Complete closeout sequence (`bd export`, `git push`, `git status`).

## Common Targets
- `make post-rebuild-check`
- `make agent-runtime-check`
- `make agent-init ISSUE=<id> ACTOR=<...>`
- `make agent-qa-check`
- `make agent-comment-checklist ISSUE=<id>`
- `NOTE="$(python .agents/skills/beads_usage/scripts/generate_note_template.py ...)" make agent-append-note ISSUE=<id>`
- `make agent-append-note ISSUE=<id> NOTE_FILE=path/to/note.md`

## Toolkit
- Target reference: `references/make_targets.md`
- Execution checklist: `assets/make_run_checklist.md`
- Suggestion helper: `scripts/suggest_make_command.py`
