---
name: blueprint_analyze_logs
description: Use this skill when the user asks to debug system errors parse large log files or generate error frequency reports.
---

# analyze-logs blueprint

## Purpose
Provide a gold-standard example skill package that demonstrates progressive disclosure and deterministic tooling.

## When to Invoke
- Use this skill when the user asks to debug system errors from raw logs.
- Use this skill when the user needs grouped error frequency and severity reporting.

## Procedure
1. Locate the user-provided log file path.
2. Run `python3 scripts/parser.py --file <path>`.
3. Cross-reference extracted error codes in `references/error-codes.md`.
4. Format final output using `assets/report-template.md`.

## Constraints
- Do not dump full raw logs into chat.
- Group findings by frequency and severity.

