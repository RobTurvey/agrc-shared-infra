---
name: beads_jira_sync
description: Use this skill when the user asks to design, implement, or operate a daily synchronization workflow between bd Beads issues and Jira issues.
---

# beads_jira_sync

## Purpose
Establish a low-cost, deterministic Jira sync process for Beads-managed work, with clear environment contracts, dry-run validation, and safe execution guidance for multi-agent sessions.

## Invoke When
- User asks to sync Beads issues into Jira on a schedule.
- User asks to reduce Jira automation rule usage while keeping Jira updated.
- User asks to create Jira tasks/comments from Beads data using REST API.
- User asks for a repeatable Jira sync runbook or skill package.

## Core Rules
- Keep Beads (`bd`) as system of record for work state.
- Prefer direct Jira REST API writes for sync (0 Jira automation usage for write path).
- If Jira automation is used, use one scheduled daily rule to stay near one execution per day.
- Manual on-demand sync is fully supported; scheduler setup is optional.
- Never print secrets/tokens in logs.
- Always support dry-run before mutating Jira.
- Ensure Jira identity marker exists in description for all synced items: `beads_id: <id>`.

## Idempotent Identity + Upsert Rule
For each Beads item `X`:
1. Search Jira for `project = DEV AND description ~ "beads_id: X"`.
2. If found, update the existing Jira issue.
3. If not found, create a new Jira issue and include `beads_id: X` in description.
4. Persist/update local mapping cache (`beads_id -> jira_key`) after every successful create/update.

## Type Classification Rule
- Classify as `epic` when:
  - Beads native type is epic/initiative, or
  - Item has children, or
  - Metadata indicates epic behavior.
- Otherwise classify as `task`.

## Jira Representation Rule (DEV)
- Preferred: create true Jira `Epic` when project configuration allows it.
- Compatibility fallback: represent Beads epic as parent `Task` with label `epic-parent`.
- Child work should use `parent` linkage to the parent Jira key whenever Jira allows it.
- Sub-task creation requires `parent` and should fail fast without parent context.

## Standard Workflow
1. Confirm source scope in Beads (for example: parent epic, labels, priority range).
2. Normalize Beads issue data to a stable sync payload.
3. Run connectivity preflight to Jira API.
4. Run dry-run payload generation and review mapped updates.
5. Execute Jira REST updates for create/update/comment as needed.
6. Apply parent-linking for children (`parent` field) when required by issue type.
7. Record sync evidence (timestamp, counts, failures) in task notes.

### Replicating an epic and child tasks
- Use `generate_sync_payload.py --epic-id <epic-id>` to include only:
  - `<epic-id>`
  - `<epic-id>.*`
- Epic records map to Jira `Epic` by default, with fallback to parent `Task` + `epic-parent` label if project constraints require.
- Child records map to `Task` or `Subtask` depending on workflow and parent requirements.

## Environment Contract
- `JIRA_BASE_URL` (example: `https://agentrealcoin.atlassian.net`)
- `JIRA_EMAIL`
- `JIRA_API_TOKEN`
- Optional fallback token key observed in local notes: `AGRC_BEADS_SYNC`

## Failure Handling
- Retry transient HTTP failures with bounded retries and jitter.
- Continue processing independent issues when one issue fails.
- Persist checkpoint/progress so reruns resume remaining work by default.
- Provide explicit full replay override when user requests restart from beginning.
- Emit per-issue result summary and final non-zero exit on hard failures.

## Toolkit
- Payload builder: `scripts/generate_sync_payload.py`
- Connectivity check: `scripts/check_jira_connectivity.py`
- Batch sync app: `scripts/sync_all_beads_to_jira.py`
- Unit tests: `scripts/test_beads_jira_sync.py`
- API contract: `references/jira_api_contract.md`
- Daily automation template: `assets/daily_sync_rule_template.md`
- Issue mapping example: `assets/issue_mapping_template.json`

## Validation Gate
- Validate package structure:
  - `python3 .agents/skills/qa_skills/scripts/validate_skill_package.py --path .agents/skills/beads_jira_sync`
