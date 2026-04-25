---
name: support_incident
description: Use this skill when the user asks to respond to a production support incident, classify severity, contain impact quickly, or draft incident communications and handoff notes.
---

# support_incident (Copilot entrypoint)

Canonical implementation is in [`.agents/skills/support_incident/SKILL.md`](.agents/skills/support_incident/SKILL.md:1).

## Behavior
1. Triage active incident scope and assign severity.
2. Prioritize containment and reversible controls.
3. Record evidence and communication cadence updates.
4. Produce structured handoff/closure notes with clear next ETA.

## Toolkit
- [`.agents/skills/support_incident/references/incident_response_runbook.md`](.agents/skills/support_incident/references/incident_response_runbook.md:1)
- [`.agents/skills/support_incident/assets/incident_update_template.md`](.agents/skills/support_incident/assets/incident_update_template.md:1)
- [`.agents/skills/support_incident/assets/severity_matrix.md`](.agents/skills/support_incident/assets/severity_matrix.md:1)
- [`.agents/skills/support_incident/scripts/prepare_incident_note.py`](.agents/skills/support_incident/scripts/prepare_incident_note.py:1)
