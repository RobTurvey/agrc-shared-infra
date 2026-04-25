# Jira Daily Sync Rule Template (Low-Cost)

## Objective
Run one scheduled Jira automation execution per day while allowing many issue updates in that single execution window.

## Rule Skeleton
- Trigger: **Scheduled**
  - Frequency: once per day (e.g., 02:00 local)
- Lookup: JQL
  - `project = DEV AND labels = from-beads`
- Branch: For each issue in lookup results
  - Apply housekeeping updates (optional)
  - Add/update digest comment (optional)

## Cost Model
- Approx. **1 execution/day** for this rule.
- Approx. **30 executions/month** at daily cadence.
- Fits under Jira free plan 100/month ceiling with margin.

## Recommended Architecture
1. Primary sync writes performed by agent using Jira REST API (create/update/comment).
2. Optional daily Jira rule used only for summarization/tidy operations.
3. Keep main state sync outside Jira Automation to preserve rule budget.

## Guardrails
- Keep JQL narrow (project + label).
- Avoid chain-triggering additional automation rules.
- Store traceability marker for Beads source (`beads_id: ...`).

