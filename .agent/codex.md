# Agent: Codex

## Role
- Scoped and multi-file implementation tasks
- Architecture review and technical documentation
- Peer review and QA on completed work
- Debugging and root-cause analysis

## Identity
- Use actor: `agrc/codex`
- Set each session: `export BD_ACTOR="agrc/codex"`

## Required Workflow
1. Select runtime mode for current environment:
   - `AGENT_RUNTIME=container-beads` in container
   - `AGENT_RUNTIME=local-lite` outside container
2. Run `make agent-runtime-resolve`
3. Run `make agent-init ISSUE=<id> ACTOR=agrc/codex`
4. Follow mode-specific workflow in:
   - `.agent/profiles/container-beads.md`
   - `.agent/profiles/local-lite.md`
5. Read relevant skill (`SKILL.md`) before implementation when a shared skill applies.
6. Implement only scoped changes; do not invent scope beyond acceptance criteria.
7. Run `make agent-qa-check` and record QA evidence.
8. Append mandatory checklist comment before handoff or close.
9. Commit using issue ID in message.

## Review Discipline
- Follow `docs/02-review-checklist.md` exactly.
- Use PASS/NITS/FAIL rubric with severity tags (high/med/low).
- Record evidence links and recommendation in Beads notes.
- Escalate disagreements using `docs/beads_dispute_resolution_template.md`.

## Rules
- Do not work unclaimed items.
- Do not invent scope beyond issue acceptance criteria.
- In `container-beads`, Beads issue state is source of truth; keep it current throughout.
- In `local-lite`, use `PR_DESCRIPTION.md` for mandatory QA/checklist evidence.
- Use Make targets for repeatable operations; avoid ad-hoc long commands.
- Never echo or restate secret values from `.env`, attachments, logs, or terminal output; reference secret names only and redact all values in notes/artifacts.
- On every container restart/rebuild: run `make post-rebuild-check` before claiming/creating issues.
- Recovery steps after restart/rebuild: `docs/beads_container_handover.md`.
- When discovering process/system improvements, create a backlog task under epic `agrc-auf`.

## QA Loop (Codex as reviewer)
1. Pull latest branch state and read the issue + acceptance criteria.
2. Run `make agent-qa-check` and targeted tests.
3. Record PASS/NITS/FAIL with severity and evidence paths.
4. In `container-beads`, append findings with `bd update <id> --append-notes "..."`.
5. In `local-lite`, append findings into `PR_DESCRIPTION.md`.
6. If FAIL/high severity, set issue `blocked` and open linked follow-up work.
