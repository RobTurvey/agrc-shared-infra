---
name: shared_infra_bootstrap
description: Use this skill when setting up agrc-shared-infra so multiple AGRC repositories can reuse skills, profiles, templates, and workflow conventions.
---

# shared_infra_bootstrap (Copilot entrypoint)

Canonical implementation is in [`.agents/skills/shared_infra_bootstrap/SKILL.md`](.agents/skills/shared_infra_bootstrap/SKILL.md).

## Behavior
1. Bootstrap shared-infra with minimum required folder layout.
2. Ensure canonical skills and Copilot entrypoints are paired.
3. Add readiness validation script and run it before handoff.
4. Confirm submodule consumption path for target repos.
