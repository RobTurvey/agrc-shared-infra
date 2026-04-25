# QA Task Review Note Template

- Decision: PASS | NITS | FAIL
- Scope reviewed:
- Acceptance criteria mapping:
  - AC1:
  - AC2:
- Findings:
  - [high|med|low] Finding title — evidence:
- Checks run:
  - `make agent-qa-check`:
  - Targeted tests:
- Runtime routing:
  - container-beads: `bd update <id> --append-notes "..." --json`
  - local-lite: update `PR_DESCRIPTION.md`
- Follow-up issue (if FAIL/high):
