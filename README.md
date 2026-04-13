# agrc-shared-infra

Shared AGRC agent infrastructure templates and reusable workflow assets.

## Purpose

This repository contains shared, reusable assets that are consumed by AGRC repositories
to keep agent workflows consistent across projects.

## Baseline Contents

- `.agents/skills/` canonical skill implementations.
- `.github/skills/` Copilot entrypoints for skill discovery.
- `.agent/profiles/` runtime profile references.
- `templates/` starter templates for new repositories.
- `scripts/` validation and bootstrap scripts.
- `Makefile.shared` common verification targets.

## Consumption Patterns

### Option 1: Git submodule (recommended)

```bash
git submodule add -b main https://github.com/RobTurvey/agrc-shared-infra.git shared-infra
```

Then reference shared content from your target repository.

### Option 2: Sync copy (fallback)

Copy required files from this repo into your project if submodules are not allowed.
Track source commit hash in your repo notes for traceability.

## Verification

Run both checks before tagging a release:

```bash
make -f Makefile.shared verify-layout
make -f Makefile.shared verify-skill
```

## Versioning Policy

- Use semantic-style baseline tags for shared snapshots.
- First baseline: `v0.1.0`.
- Increment patch for docs/tooling fixes (`v0.1.1`).
- Increment minor for new templates/skills (`v0.2.0`).

## Release Steps

```bash
git add .
git commit -m "chore: baseline shared infra v0.1.0"
git push
git tag v0.1.0
git push origin v0.1.0
```
