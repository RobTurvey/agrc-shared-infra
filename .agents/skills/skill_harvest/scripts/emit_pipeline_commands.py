#!/usr/bin/env python3
"""Emit deterministic skill_harvest command templates.

This script prints command sequences only. It does not execute them.
"""

from __future__ import annotations

import argparse


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit skill_harvest command templates")
    parser.add_argument("--source-url", help="External source URL")
    parser.add_argument("--candidate-id", help="Candidate ID from fetch receipt")
    parser.add_argument("--skill-id", help="Skill ID in live index")
    parser.add_argument("--issue", help="Optional Beads issue ID")
    args = parser.parse_args()

    print("# 1) Fetch")
    print(
        "python3 .agents/skill_harvest/scripts/fetch_external_skill.py "
        f"--url {args.source_url or '<source-url>'} --fetch-linked"
        + (f" --issue {args.issue}" if args.issue else "")
    )

    print("\n# 2) Analyze")
    print(
        "python3 .agents/skill_harvest/scripts/analyze_harvested_skill.py "
        f"--candidate-id {args.candidate_id or '<candidate-id>'}"
    )

    print("\n# 3) QA")
    print(
        "python3 .agents/skill_harvest/scripts/qa_validate_harvested_skill.py "
        f"--candidate-id {args.candidate_id or '<candidate-id>'}"
    )

    print("\n# 4) Approval package + decision")
    print(
        "python3 .agents/skill_harvest/scripts/build_approval_package.py "
        f"--candidate-id {args.candidate_id or '<candidate-id>'}"
    )
    print(
        "python3 .agents/skill_harvest/scripts/record_approval_decision.py "
        f"--candidate-id {args.candidate_id or '<candidate-id>'} "
        "--decision approve --rationale \"<why approved>\""
    )

    print("\n# 5) Register + publish")
    print(
        "python3 .agents/skill_harvest/scripts/register_approved_skill.py "
        f"--candidate-id {args.candidate_id or '<candidate-id>'}"
    )
    print(
        "python3 .agents/skill_harvest/scripts/publish_live_skill.py "
        f"--skill-id {args.skill_id or '<skill-id>'} --force"
        + (f" --issue {args.issue}" if args.issue else "")
    )

    print("\n# 6) Policy check")
    print("python3 .agents/skill_harvest/scripts/check_governance_policy.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
