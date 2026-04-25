import argparse
from pathlib import Path


SKILL_TEMPLATE = """---
name: {name}
description: Use this skill when the user asks to {trigger_a} or needs to {trigger_b}.
---

# {name}

## Purpose
{purpose}

## When to Invoke
- Use this skill when the user asks to {trigger_a}.
- Use this skill when the user needs to {trigger_b}.

## Inputs
- User objective
- Constraints and guardrails

## Outputs
- Structured result with deterministic format

## Procedure
1. Confirm scope and expected outcome.
2. Execute repeatable steps.
3. Validate output quality.
4. Return concise final result.
"""


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def scaffold(base_dir: Path, skill_name: str, purpose: str, trigger_a: str, trigger_b: str) -> Path:
    target = base_dir / skill_name
    ensure_dir(target)
    ensure_dir(target / "scripts")
    ensure_dir(target / "references")
    ensure_dir(target / "assets")

    skill_md = target / "SKILL.md"
    write_if_missing(
        skill_md,
        SKILL_TEMPLATE.format(
            name=skill_name,
            purpose=purpose,
            trigger_a=trigger_a,
            trigger_b=trigger_b,
        ),
    )

    write_if_missing(target / "references" / "README.md", "# References\n\nAdd deep context here.\n")
    write_if_missing(target / "assets" / "README.md", "# Assets\n\nAdd templates/examples here.\n")
    write_if_missing(
        target / "scripts" / "README.md",
        "# Scripts\n\nAdd deterministic scripts with --help and non-zero failures.\n",
    )

    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new skill scaffold")
    parser.add_argument("--base-dir", default=".agents/skills", help="Root directory for skill packages")
    parser.add_argument("--name", required=True, help="Skill folder and metadata name")
    parser.add_argument("--purpose", required=True, help="Short purpose statement")
    parser.add_argument("--trigger-a", required=True, help="Primary activation intent")
    parser.add_argument("--trigger-b", required=True, help="Secondary activation intent")
    args = parser.parse_args()

    target = scaffold(
        Path(args.base_dir),
        args.name.strip(),
        args.purpose.strip(),
        args.trigger_a.strip(),
        args.trigger_b.strip(),
    )
    print(f"Created skill scaffold at: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

