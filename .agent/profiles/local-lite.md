# Profile: local-lite

Use this profile when running outside the devcontainer.

## Rules
- Do not depend on `bd` commands in local-lite flows.
- Keep a local worklog and sync updates to Beads from container-beads mode.
- Prioritize read-only diagnostics and safe deployment actions.

## Startup Sequence
1. `AGENT_RUNTIME=local-lite make agent-runtime-resolve`
2. Perform local-only work (for example host tooling or AWS operations).
3. Transfer progress to Beads from container-beads environment.

## Closeout
- Ensure code changes are pushed.
- Ensure Beads issue notes are updated from a container-beads environment.
