# Profile: container-beads

Use this profile when running in a devcontainer where Beads is available.

## Rules
- `bd` is required for issue tracking updates.
- Run runtime preflight before task work.
- Keep issue comments and notes current for milestones and handoff.

## Startup Sequence
1. `make agent-runtime-resolve`
2. `make agent-init ISSUE=<id> ACTOR=<agrc/copilot|agrc/roo|agrc/claude>`
3. Run implementation and validation commands.

## Closeout
1. `bd export -o .beads/issues.jsonl`
2. `git pull --rebase`
3. `git push`
