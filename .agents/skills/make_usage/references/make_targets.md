# Make Target Reference

## Runtime and Init
- `make agent-runtime-check`
- `make agent-init ISSUE=<id> ACTOR=<agrc/copilot|agrc/codex|agrc/claude>`
- `make post-rebuild-check`

## QA and Notes
- `make agent-qa-check`
- `make agent-comment-checklist ISSUE=<id>`
- `NOTE="$(python .agents/skills/beads_usage/scripts/generate_note_template.py ...)" make agent-append-note ISSUE=<id>`
- `make agent-append-note ISSUE=<id> NOTE_FILE=path/to/note.md`

## Beads Wrappers
- `make mem-ready`
- `make mem-show ISSUE=<id>`
- `make mem-claim ISSUE=<id>`
- `make mem-close ISSUE=<id>`
- `make mem-handoff`

## Runtime Override
- `AGENT_RUNTIME=local-lite make agent-runtime-check`
- `AGENT_RUNTIME=local-lite make agent-init ISSUE=<id> ACTOR=<agrc/codex>`
