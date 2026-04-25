# Jira API Contract for Beads Sync

## Base Endpoint
- `JIRA_BASE_URL` + `/rest/api/3`

## Authentication
- Basic auth using Atlassian email + API token.
- Header pattern:
  - `Authorization: Basic <base64(email:token)>`
  - `Content-Type: application/json`

## Required Environment Variables
- `JIRA_BASE_URL`
- `JIRA_EMAIL`
- `JIRA_API_TOKEN`

## Optional Environment Variables
- `JIRA_PROJECT_KEY` (default `DEV`)
- `JIRA_SYNC_LABEL` (default `from-beads`)
- `JIRA_BEADS_PARENT_EPIC` (example `agrc-auf`)
- `AGRC_BEADS_SYNC` (fallback token key if used in local env)

## Operations Used by Sync

### 1) Search existing Jira issues
- `GET /search/jql` (preferred in this workspace)
- `POST /search` (compatibility option where enabled)
- Purpose: find candidate issues by project + marker-based identity.

Recommended query intent:
- `project = DEV AND description ~ "beads_id: <id>"`

Identity rule:
- Every synced issue description must contain `beads_id: <id>` as a stable idempotent lookup marker.

### 2) Create issue
- `POST /issue`
- Required fields:
  - `fields.project.key`
  - `fields.summary`
  - `fields.issuetype.name`

Recommended fields:
- `fields.description` (ADF)
- `fields.labels` includes `from-beads`

Type guidance for DEV:
- Prefer Jira `Epic` when allowed by project config.
- If Epic is unavailable/blocked, fallback to parent `Task` with label `epic-parent`.
- For Sub-task creation, include `fields.parent.key`.

### 3) Update issue
- `PUT /issue/{issueIdOrKey}`
- Use idempotent updates for summary/description/labels/status mapping fields where permitted.

### 4) Add comment
- `POST /issue/{issueIdOrKey}/comment`
- Use for Beads status digest and traceability updates.

## Data Mapping Guidance
- Beads ID -> Jira external reference marker in description or comment (e.g. `beads_id: agrc-auf.3`).
- Beads title -> Jira summary.
- Beads description -> Jira description.
- Beads priority -> Jira priority (policy mapping configurable).
- Beads status -> Jira status transition policy (optional, project workflow dependent).

Day-2 update rule:
- Cache `beads_id -> jira_key` locally after successful create/update.
- On subsequent sync, use cache-first lookup and fallback to marker search if cache miss/stale.

Parent-child linking:
- If Beads item is epic-like parent, map to Jira Epic (or fallback parent Task).
- For child items, set `parent` to mapped Jira key when issue type requires/permits it.

## Reliability + Safety
- Always run dry-run generation before first write.
- Avoid destructive field overwrites unless explicitly configured.
- Do not log raw auth tokens.
- Return non-zero exit code when any hard failure occurs.
