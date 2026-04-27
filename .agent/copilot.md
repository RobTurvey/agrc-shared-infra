# Agent: GitHub Copilot

## Role
- Complex feature work and architectural changes
- Multi-file refactors
- Debugging and peer reviews

## Required Workflow
1. Select runtime mode for current environment:
	- `AGENT_RUNTIME=container-beads` in container
	- `AGENT_RUNTIME=local-lite` outside container
2. `make agent-runtime-check`
3. `make agent-init ISSUE=<id> ACTOR=agrc/copilot`
4. Follow mode-specific workflow in:
	- `.agent/profiles/container-beads.md`
	- `.agent/profiles/local-lite.md`
5. Confirm scope + acceptance criteria from issue
6. Implement and commit with issue ID in message
7. Run `make agent-qa-check` and record QA evidence

## Review Discipline
- Follow `docs/02-review-checklist.md` exactly
- Use PASS/NITS/FAIL rubric
- Record severity for findings (high/med/low)

## Rules
- In `container-beads`, Beads issue state is source of truth
- In `local-lite`, use `PR_DESCRIPTION.md` for mandatory QA/checklist evidence
- Use Make targets for repeatable operations; avoid ad-hoc long commands
- Never echo or restate secret values from `.env`, attachments, logs, or terminal output; reference secret names only and redact all values in notes/artifacts
- On every container restart/rebuild: run `make post-rebuild-check` before claiming/creating issues
- If UI is needed after restart: run `make beads-ui-restart`
- When discovering process/system improvements, create a backlog task under epic `agrc-auf`
- Recovery steps after restart/rebuild: `docs/beads_container_handover.md`
- Container restart + validation checks: `docs/build/docker_container_tips.md`
- AWS in-container incident runbook: `docs/aws_auction_emergency_stop_floor_reset_replay_playbook.md`
