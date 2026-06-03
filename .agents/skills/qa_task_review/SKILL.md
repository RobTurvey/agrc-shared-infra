---
name: qa_task_review
description: Use this skill when the user asks to review another agent's completed feature work for task acceptance or needs to produce a QA decision with severity-tagged findings and evidence.
---

# qa_task_review

## Purpose
Run Codex-ready QA reviews for completed implementation tasks with deterministic evidence and PASS/NITS/FAIL outcomes.

## When to Invoke
- User asks to review Copilot/agent-delivered task work before handoff.
- User asks for a structured QA decision mapped to acceptance criteria.
- User asks for evidence-backed PASS/NITS/FAIL findings with severity tags.

## Inputs
- Issue ID and acceptance criteria
- Changed files/PR scope
- Runtime mode (`container-beads` or `local-lite`)

## Outputs
- QA decision: PASS, NITS, or FAIL
- Findings with severity: `high`, `med`, `low`
- Evidence list (commands, files, test outputs)
- Handoff note text for Beads or PR description

## Procedure
1. Confirm scope from issue acceptance criteria and changed files.
2. Follow review checklist in `references/review_process.md` and `docs/02-review-checklist.md`.
3. Run deterministic checks: `make agent-qa-check` plus targeted tests for changed areas.
4. Classify findings as PASS/NITS/FAIL with severity tags and evidence paths.
5. Produce reviewer note using `assets/qa_task_review_note_template.md`.
6. In `container-beads`, append note with `bd update <id> --append-notes "..." --json`; in `local-lite`, update `PR_DESCRIPTION.md`.
7. If FAIL/high severity, mark blocked and create linked follow-up issue (`--deps discovered-from:<id>`).

## Toolkit
- Process reference: `references/review_process.md`
- Findings template: `assets/qa_task_review_note_template.md`
- Note helper: `scripts/generate_qa_review_note.py`

## Agent Execution Rule
- Always include explicit acceptance-criteria mapping and at least one concrete evidence item per finding.
