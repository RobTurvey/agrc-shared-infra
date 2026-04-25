# Beads Task Checklist

## Intake
- [ ] Runtime selected (`container-beads` or `local-lite`)
- [ ] Initialization run (`make agent-runtime-check`, `make agent-init ...`)
- [ ] Ready work inspected (`bd ready --json`)

## Work Tracking
- [ ] Task claimed (`bd update <id> --status in_progress --json`)
- [ ] Discovered work linked with `discovered-from`
- [ ] Priority/status updated as needed

## Validation and Notes
- [ ] QA checks executed and result captured
- [ ] Mandatory note bullets prepared
- [ ] Note appended with `make agent-append-note`

## Closeout
- [ ] Task closed with reason
- [ ] `bd export -o .beads/issues.jsonl`
- [ ] `git pull --rebase && git push`
- [ ] `git status` confirms up-to-date

