# Incident Response Runbook

## Pause/Resume Control Rationale

1. Risk containment: pause halts new state transitions when bad inputs, pricing anomalies, signer issues, or dependency failures are detected.
2. Blast-radius reduction: a quick pause avoids cascading incorrect listings, settlements, and reporting side effects.
3. Recovery without redeploy: resume lets teams continue from a known-good state after validation checks.
4. Operational discipline: drill pause/resume regularly so execution is reliable under production stress.
5. Auditability: pause and resume events provide a clear timeline for incident review and readiness evidence.

## Severity Matrix

- Sev-0: Safety or security emergency, broad active impact, or irreversible data risk.
  - Action target: immediate containment and executive escalation.
- Sev-1: Major customer-facing outage or high error rate in core flows.
  - Action target: containment in minutes and frequent status updates.
- Sev-2: Partial degradation with workaround available.
  - Action target: mitigate quickly, reduce recurring impact.
- Sev-3: Minor operational issue, no meaningful customer impact.
  - Action target: schedule fix via normal priority.

## Triage Checklist

1. What changed recently?
2. What is failing and for whom?
3. Is impact growing right now?
4. Which reversible controls are available?
5. What evidence proves containment?

## Containment Patterns

1. Toggle pause mode to stop unsafe transitions.
2. Disable non-critical paths or scheduled jobs.
3. Route around unhealthy dependency where safe.
4. Lower throughput to stabilize while preserving core service.

## Pause/Resume Procedure

1. Trigger pause when impact is active or uncertainty is high.
2. Record pause event timestamp and reason.
3. Run validation checks until impact growth has stopped.
4. Apply minimal remediation and verify core path health.
5. Resume only when checks pass and rollback path is defined.
6. Record resume timestamp, validation evidence, and owner approval.

## Communication Cadence

1. Initial update within 10 minutes of incident declaration.
2. Ongoing updates every 15-30 minutes by severity.
3. Each update includes impact, what changed, and next ETA.

## Evidence Expectations

1. Timeline entries with UTC timestamps.
2. Commands run and notable outputs (redacted).
3. Validation proof that impact stopped expanding.
4. Residual risk and owner for follow-up work.
