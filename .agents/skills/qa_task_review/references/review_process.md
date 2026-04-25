# QA Task Review Process (Roo)

## Source of Truth
- `.agent/roo.md` (QA Loop + Review Discipline)
- `docs/02-review-checklist.md`

## Steps
1. Read issue acceptance criteria and changed files.
2. Run `make agent-qa-check` and focused tests for affected components.
3. Record findings as PASS/NITS/FAIL with severity tags (`high`/`med`/`low`).
4. Attach evidence paths (files, command outputs, test logs).
5. Route review output by runtime:
   - `container-beads`: append findings via `bd update <id> --append-notes "..." --json`
   - `local-lite`: append findings to `PR_DESCRIPTION.md`
6. For FAIL/high severity, mark blocked and create a linked follow-up issue with `--deps discovered-from:<id>`.

## Severity Guidance
- `high`: acceptance criteria failure, security/data integrity risk, broken critical path.
- `med`: functional or reliability concern with workaround.
- `low`: clarity, docs, or minor polish improvement.
