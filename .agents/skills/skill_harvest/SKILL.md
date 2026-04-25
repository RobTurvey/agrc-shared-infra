---
name: skill_harvest
description: Use this skill when the user asks to harvest, assess, approve, register, or publish external skills through the governed .agents/skill_harvest pipeline.
---

# skill_harvest

## Purpose

Provide a deterministic, auditable workflow for external skill ingestion without bypassing governance controls.

## Use When

- The user asks to import or evaluate a skill from an external source.
- The user asks to run or repeat the fetch -> analysis -> QA -> approval -> register -> publish flow.
- The user asks how a live skill got into agent discovery paths.

## Do Not Use When

- The user is creating a brand-new local skill from scratch (use `skills_creator`).
- The request is normal feature coding unrelated to external skill governance.

## Required Inputs

- `source_url` or known candidate ID
- optional Beads issue ID for evidence comments

## Governance Guardrails

- Never execute fetched content.
- Never load from inbox, reports, or URL at runtime.
- Only publish from approved/live registry artifacts.
- Preserve evidence artifacts for each stage.

## Workflow

1. Fetch candidate into quarantine inbox.
2. Run static analysis and capture risk score.
3. Run deterministic QA validation.
4. Build approval package and record human decision.
5. Register approved candidate into approved/live registry.
6. Publish live skill into discovery paths:
- `.agents/skills/<skill_id>/SKILL.md`
- `.github/skills/<skill_id>/skill.md`
7. Run governance policy check.

## Canonical Commands

Use [pipeline_commands.md](references/pipeline_commands.md) for exact command templates.

## Outputs

- Candidate receipts in `.agents/skill_harvest/inbox/` and `.agents/skill_harvest/reports/`
- Live registry entries in `.agents/skill_harvest/live/skill_index.json`
- Discovery-path skill files under `.agents/skills/` and `.github/skills/`
