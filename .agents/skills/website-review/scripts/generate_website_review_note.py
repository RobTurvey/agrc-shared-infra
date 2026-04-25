#!/usr/bin/env python3
"""Generate a concise markdown note for website review status updates.

Usage:
  python .agents/skills/website-review/scripts/generate_website_review_note.py \
    --target "http://127.0.0.1:4321/" \
    --report "docs/reports/example.md" \
    --evidence "artifacts/site-audit/.../audit.json" \
    --top-findings "Missing H1; Mobile overflow"
"""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate website review markdown note")
    parser.add_argument("--target", required=True, help="Reviewed target URL")
    parser.add_argument("--report", required=True, help="Path to markdown report")
    parser.add_argument("--evidence", required=True, help="Path to primary evidence artifact")
    parser.add_argument("--top-findings", required=True, help="Semicolon-separated top findings")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    findings = [item.strip() for item in args.top_findings.split(";") if item.strip()]

    print("## Website Review Update")
    print(f"- Target: {args.target}")
    print(f"- Report: {args.report}")
    print(f"- Evidence: {args.evidence}")
    print("- Top findings:")
    if findings:
        for finding in findings:
            print(f"  - {finding}")
    else:
        print("  - None")
    print("- Next step: Prioritize remediation and re-run audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

