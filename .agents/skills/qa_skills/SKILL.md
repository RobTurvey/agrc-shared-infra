---
name: qa_skills
description: Use this skill when the user asks to review a process or skill package for quality compliance or needs a deterministic QA report before handoff.
---

# qa_skills

## Purpose
Run a repeatable quality assurance review for skills and process changes with evidence-first reporting.

## When to Invoke
- User asks for review/QA of an existing process or skill package.
- User asks to validate a newly created skill against repository conventions.
- User asks for pass/fail findings with actionable remediation items.

## Inputs
- Target path(s) to review
- Review scope (process, skill package, or both)
- Repository guardrails and mandatory checklists

## Outputs
- QA report with: checks run, findings, severity, evidence, remediation
- Pass/fail decision with explicit acceptance criteria mapping

## Procedure
1. Confirm QA scope and acceptance criteria.
2. Run deterministic checks using `python3 .agents/skills/qa_skills/scripts/validate_skill_package.py --help` semantics.
3. Review process compliance against the rubric in `references/qa_rubric.md`.
4. Produce a report using `assets/qa_report_template.md`.
5. Return a concise final decision with remediation tasks.

## Toolkit
- Rubric: `references/qa_rubric.md`
- Report template: `assets/qa_report_template.md`
- Validator script: `scripts/validate_skill_package.py`

## Agent Execution Rule
- For skill-package QA, run the validator script first and include its concrete failures/warnings in the final report.
