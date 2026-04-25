# Beads Command Reference

## Intake and Claim
- `bd ready --json`
- `bd show <id> --json`
- `bd update <id> --status in_progress --json`
- `bd comments add <id> "Started by <actor>: <scope>"`

## Create and Link Work
- `bd create "Title" --description="Context" -t task -p 2 --json`
- `bd create "Found follow-up" --description="Details" -p 1 --deps discovered-from:<parent-id> --json`

## Progress and Closure
- `bd update <id> --priority <0-4> --json`
- `bd comments add <id> "Milestone: <what changed>; Evidence: <artifact/log>"`
- `bd comments add <id> "Blocker: <impact>; Needed: <unblock>"`
- `bd close <id> --reason "Completed" --json`

## Notes and Checklist
- Comments are for timeline/audit events (who did what and when).
- Notes are for structured handoff/closure summaries.
- Keep notes human-readable with real multiline bullets or markdown headings.
- `make agent-comment-checklist ISSUE=<id>`
- `NOTE="$(python .agents/skills/beads_usage/scripts/generate_note_template.py --done '...' --files '...' --validation '...' --risks 'None' --next-step 'None')" make agent-append-note ISSUE=<id>`
- You may also use `make agent-append-note ISSUE=<id> NOTE_FILE=path/to/note.md`

## Closeout Sequence
1. `git pull --rebase`
2. `bd export -o .beads/issues.jsonl`
3. `git push`
4. `git status`

