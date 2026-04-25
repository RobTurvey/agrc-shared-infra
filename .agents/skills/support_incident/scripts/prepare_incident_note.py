#!/usr/bin/env python3
"""Generate a structured incident note block for timeline and handoff updates."""

import argparse
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a production incident status note")
    parser.add_argument("--title", required=True, help="Incident title or ID")
    parser.add_argument("--severity", required=True, choices=["Sev-0", "Sev-1", "Sev-2", "Sev-3"])
    parser.add_argument("--impact", required=True, help="Current user/system impact")
    parser.add_argument("--status", required=True, choices=["investigating", "contained", "recovering", "resolved"])
    parser.add_argument("--actions", required=True, help="Semicolon-separated actions taken")
    parser.add_argument("--evidence", required=True, help="Comma-separated evidence references")
    parser.add_argument("--risks", default="None", help="Known risks or blockers")
    parser.add_argument("--next-eta", required=True, help="Next update ETA in UTC format")
    parser.add_argument("--owner", required=True, help="Incident owner")
    args = parser.parse_args()

    actions = [item.strip() for item in args.actions.split(";") if item.strip()]
    evidence = [item.strip() for item in args.evidence.split(",") if item.strip()]

    print(f"- Time (UTC): {utc_now()}")
    print(f"- Incident ID/Title: {args.title}")
    print(f"- Severity: {args.severity}")
    print(f"- Impact: {args.impact}")
    print(f"- Current status: {args.status}")
    print("- Actions taken since last update: " + ("; ".join(actions) if actions else "None"))
    print("- Evidence: " + (", ".join(evidence) if evidence else "None"))
    print(f"- Risks or blockers: {args.risks}")
    print(f"- Next update ETA (UTC): {args.next_eta}")
    print(f"- Owner: {args.owner}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
