---
name: beads_usage
description: Use this skill when the user asks to manage work with bd beads including intake claiming updates closure dependency linking and mandatory status notes.
---

# beads_usage

## Purpose
Apply the repository's required Beads workflow as the single source of truth for issue tracking and handoff discipline.

## Invoke When
- User asks what to work on next with Beads.
- User asks to claim update or close a Beads issue.
- User asks to create discovered follow-up work linked to a parent issue.
- Session is ending and Beads status notes plus closeout steps are required.

## Core Rules
- Use `bd` for all issue tracking in this repo.
- Always include `--json` for Beads commands.
- Link discovered work with `--deps discovered-from:<parent-id>`.
- Do not create markdown TODO trackers as the system of record.
- Use `bd comments add` for chronological event logging (who did what and when).
- Use notes for structured checklist summaries and closure/handoff state.
- Notes must be human-readable markdown with real line breaks, bullets, and headings when helpful.
- Never leave literal `\n` escape sequences visible in the saved Beads note.

## Standard Workflow
1. Detect runtime and initialize task context when needed.
2. Find ready work with `bd ready --json`.
3. Claim issue: `bd update <id> --status in_progress --json`.
4. Add a start comment: `bd comments add <id> "Started by <actor>: <scope>"`.
5. Execute implementation and validation.
6. Add milestone/blocker comments with timestamps and evidence pointers.
7. Append mandatory status note bullets.
8. Close issue: `bd close <id> --reason "Completed" --json`.

## Mandatory Session Closeout
1. `git pull --rebase`
2. `bd export -o .beads/issues.jsonl`
3. `git push`
4. `git status` must indicate up-to-date with origin

## Toolkit
- Commands reference: `references/beads_commands.md`
- Checklist template: `assets/beads_task_checklist.md`
- Note helper script: `scripts/generate_note_template.py`

## Agent Execution Rule
- When preparing mandatory Beads note text, the agent should run `python .agents/skills/beads_usage/scripts/generate_note_template.py ...` and pass the multiline output directly into the note append step.
- Prefer `make agent-append-note ISSUE=<id> NOTE="$(python ... )"` or `NOTE_FILE=<path>` so formatting is preserved for humans.
- If note text contains escaped newlines like `\n`, normalize them before saving so the final Beads note renders as readable multiline markdown.
- Agents should treat comments as the audit timeline and notes as structured summaries; both are required for non-trivial tasks.
