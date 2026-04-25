# QA Rubric for Process and Skill Reviews

## 1) Scope and Traceability
- Scope is explicitly stated (what is in/out).
- Acceptance criteria are listed and testable.
- Findings map to criteria with evidence.

## 2) Skill Package Structure
- Required package layout exists (`SKILL.md`, `scripts/`, `references/`, `assets/`).
- Folder name matches frontmatter `name`.
- `description` begins with `Use this skill when...`.
- Activation includes at least two concrete intent patterns.

## 3) Instruction Quality
- Steps are deterministic and executable.
- Ambiguous language is minimized.
- Guardrails and constraints are preserved.
- Outputs are defined with clear expected format.

## 4) Script Quality (if scripts exist)
- Script supports `--help`.
- Non-zero exit codes on failures.
- Inputs are validated with clear error messages.

## 5) Evidence and Decision
- Report includes command/check outputs or direct file evidence.
- Severity assigned to each finding (`critical`, `major`, `minor`).
- Final decision states `pass` or `fail` with remediation list.
