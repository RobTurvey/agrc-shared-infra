---
name: beads_jira_sync
description: Use this skill when the user asks to set up or run daily synchronization between bd Beads work items and Jira issues.
---

# beads_jira_sync (Copilot entrypoint)

Use the shared implementation in [`.agents/skills/beads_jira_sync/SKILL.md`](../../../.agents/skills/beads_jira_sync/SKILL.md) as the canonical source.

## Behavior
1. Treat Beads as source of truth and Jira as synchronized mirror.
2. Prefer direct Jira REST API writes for sync operations.
3. Prefer manual on-demand sync app execution; Jira Automation is optional housekeeping only.
4. Run dry-run payload generation before mutating Jira.
5. Use `beads_id: <id>` marker in Jira description for idempotent find/update.
6. Use cache-first mapping (`beads_id -> jira_key`) with marker-search fallback.
7. Use checkpoint/resume so reruns continue remaining work after partial failure.
8. Capture evidence and failures for deterministic handoff.

## Shared Toolkit
- [`.agents/skills/beads_jira_sync/scripts/generate_sync_payload.py`](../../../.agents/skills/beads_jira_sync/scripts/generate_sync_payload.py)
- [`.agents/skills/beads_jira_sync/scripts/check_jira_connectivity.py`](../../../.agents/skills/beads_jira_sync/scripts/check_jira_connectivity.py)
- [`.agents/skills/beads_jira_sync/scripts/sync_all_beads_to_jira.py`](../../../.agents/skills/beads_jira_sync/scripts/sync_all_beads_to_jira.py)
- [`.agents/skills/beads_jira_sync/scripts/test_beads_jira_sync.py`](../../../.agents/skills/beads_jira_sync/scripts/test_beads_jira_sync.py)
- [`.agents/skills/beads_jira_sync/references/jira_api_contract.md`](../../../.agents/skills/beads_jira_sync/references/jira_api_contract.md)
- [`.agents/skills/beads_jira_sync/assets/daily_sync_rule_template.md`](../../../.agents/skills/beads_jira_sync/assets/daily_sync_rule_template.md)
- [`.agents/skills/beads_jira_sync/assets/issue_mapping_template.json`](../../../.agents/skills/beads_jira_sync/assets/issue_mapping_template.json)
