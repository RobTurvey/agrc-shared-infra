---
name: support_incident
description: Use this skill when the user asks to respond to a production support incident, run incident triage with severity and containment, or prepare stakeholder incident updates and handoff notes.
---

# support_incident

## Purpose
Provide a fast, repeatable production incident workflow with clear severity, containment, communication, and closure checkpoints.

## Invoke When
- Use this skill when the user asks to triage a production outage, degradation, or data inconsistency.
- Use this skill when the user asks to run incident response steps, communications, or post-incident handoff notes.

## Do Not Invoke
- Normal feature development tasks that are not time-sensitive operations incidents.
- Planned release checklists that do not include an active production impact.

## Response Priorities
1. Safety first: prevent further harm before root-cause depth work.
2. Time-to-containment over time-to-perfect-fix.
3. Explicit communication cadence with timestamped updates.
4. Preserve evidence for follow-up review.

## Why Pause/Resume Is Critical
1. Risk containment: pause stops new state transitions when bad inputs, pricing anomalies, signer issues, or dependency failures are detected.
2. Blast-radius reduction: pause prevents a small fault from cascading into incorrect listings, settlements, or reporting records.
3. Recovery without redeploy: resume restarts from a verified-good state after checks, avoiding disruptive emergency redeploy behavior.
4. Operational discipline: regular pause/resume drills prove the runbook can be executed under pressure.
5. Auditability and trust: each pause/resume action provides a clear timeline for incident review and launch evidence.
6. Launch confidence: reliable pause/resume controls allow faster decisions with a bounded fallback path.

## Standard Workflow
1. Confirm incident scope.
   - Capture impacted system, first-seen time, user impact, and blast radius.
2. Assign severity.
   - Use the matrix in `references/incident_response_runbook.md`.
3. Execute containment.
   - Prefer reversible, low-risk controls (pause, feature flag disable, traffic isolation).
   - If unsafe transitions are active, issue pause first before deeper diagnosis.
4. Validate containment.
   - Prove customer impact is no longer increasing.
5. Stabilize service.
   - Apply minimal safe remediation to restore core path.
6. Resume guarded operations.
   - Resume only after validation checks pass and rollback path is clear.
7. Communicate status.
   - Send concise updates using `assets/incident_update_template.md`.
8. Capture handoff and closure notes.
   - Include timeline, commands run, outcomes, risks, and next steps.

## Required Output Format
Return incident output with these sections:
1. Incident summary
2. Severity and rationale
3. Containment actions taken
4. Pause/resume state and rationale
5. Current customer impact
6. Evidence collected
7. Next update ETA
8. Handoff/owner and next steps

## Toolkit
- Runbook: `references/incident_response_runbook.md`
- Status template: `assets/incident_update_template.md`
- Severity matrix: `assets/severity_matrix.md`
- Note helper: `scripts/prepare_incident_note.py`

## Validation Gate
- Confirm no secret values are echoed in incident updates.
- Confirm the output includes explicit next update ETA.
- Confirm at least one containment validation check is recorded.
