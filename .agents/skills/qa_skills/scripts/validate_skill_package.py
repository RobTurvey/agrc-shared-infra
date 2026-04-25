import argparse
import re
from pathlib import Path


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")


def warn(msg: str) -> None:
    print(f"WARN: {msg}")


def ok(msg: str) -> None:
    print(f"OK: {msg}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_frontmatter(skill_md_text: str, expected_name: str) -> list[str]:
    issues: list[str] = []
    if not skill_md_text.startswith("---"):
        issues.append("SKILL.md must start with YAML frontmatter delimiter '---'.")
        return issues

    m = re.match(r"^---\n(.*?)\n---\n", skill_md_text, flags=re.DOTALL)
    if not m:
        issues.append("SKILL.md has invalid or unclosed YAML frontmatter block.")
        return issues

    fm = m.group(1)
    name_match = re.search(r"^name:\s*(.+)$", fm, flags=re.MULTILINE)
    desc_match = re.search(r"^description:\s*(.+)$", fm, flags=re.MULTILINE)

    if not name_match:
        issues.append("Frontmatter missing 'name'.")
    else:
        name = name_match.group(1).strip().strip('"').strip("'")
        if name != expected_name:
            issues.append(f"Frontmatter name '{name}' does not match folder '{expected_name}'.")

    if not desc_match:
        issues.append("Frontmatter missing 'description'.")
    else:
        desc = desc_match.group(1).strip().strip('"').strip("'")
        if not desc.startswith("Use this skill when"):
            issues.append("Description must start with 'Use this skill when'.")

    return issues


def count_activation_intents(skill_md_text: str) -> int:
    pattern = re.compile(r"^\s*-\s+.*(user asks|user needs|asks to|needs to).*$", flags=re.IGNORECASE | re.MULTILINE)
    return len(pattern.findall(skill_md_text))


def validate_package(path: Path) -> int:
    errors = 0

    if not path.exists() or not path.is_dir():
        fail(f"Path does not exist or is not a directory: {path}")
        return 2

    expected = ["SKILL.md", "scripts", "references", "assets"]
    for entry in expected:
        p = path / entry
        if not p.exists():
            fail(f"Missing required entry: {entry}")
            errors += 1
        else:
            ok(f"Found required entry: {entry}")

    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        return 1

    text = read_text(skill_md)
    fm_issues = validate_frontmatter(text, path.name)
    for issue in fm_issues:
        fail(issue)
        errors += 1

    intents = count_activation_intents(text)
    if intents < 2:
        fail(f"Expected at least 2 activation intent lines; found {intents}.")
        errors += 1
    else:
        ok(f"Activation intent lines found: {intents}")

    scripts_dir = path / "scripts"
    if scripts_dir.exists() and scripts_dir.is_dir():
        py_scripts = [p for p in scripts_dir.glob("*.py")]
        for script in py_scripts:
            content = read_text(script)
            if "ArgumentParser" not in content and "argparse" not in content:
                warn(f"Script may not provide --help via argparse: {script.name}")

    if errors:
        print(f"\nValidation completed with {errors} error(s).")
        return 1

    print("\nValidation passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a skill package against repository QA conventions")
    parser.add_argument("--path", required=True, help="Path to skill package (e.g. .agents/skills/qa)")
    args = parser.parse_args()
    return validate_package(Path(args.path))


if __name__ == "__main__":
    raise SystemExit(main())

