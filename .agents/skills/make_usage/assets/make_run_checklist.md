# Make Run Checklist

## Before Running
- [ ] Goal mapped to correct target
- [ ] Required variables provided (`ISSUE`, `ACTOR`, `NOTE`)
- [ ] Runtime selected (`container-beads` or `local-lite`)

## Execution
- [ ] `make agent-runtime-check`
- [ ] `make agent-init ISSUE=<id> ACTOR=<...>`
- [ ] Run selected target and capture output

## After Running
- [ ] QA evidence captured if code changed
- [ ] Mandatory note/checklist completed
- [ ] Handoff and push sequence completed when ending session

