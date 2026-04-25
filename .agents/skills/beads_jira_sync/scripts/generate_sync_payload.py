#!/usr/bin/env python3
"""Generate deterministic Jira sync payloads from Beads issues JSON.

Input can be any JSON array containing issue objects with keys like:
id, title, description, status, priority.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Jira sync payloads from Beads issues JSON"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to Beads issues JSON file (array of issue objects)",
    )
    parser.add_argument(
        "--project-key",
        default="DEV",
        help="Jira project key (default: DEV)",
    )
    parser.add_argument(
        "--label",
        default="from-beads",
        help="Jira label to apply (default: from-beads)",
    )
    parser.add_argument(
        "--output",
        default="-",
        help="Output file path or '-' for stdout (default: -)",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=0,
        help="Optional max number of issues to transform (0 = all)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Emit payload with dry_run=true metadata",
    )
    parser.add_argument(
        "--only-ids",
        default="",
        help="Comma-separated Beads issue IDs to include (default: all)",
    )
    parser.add_argument(
        "--epic-id",
        default="",
        help="Replicate one Beads epic and children (matches <epic-id> and <epic-id>.*)",
    )
    return parser.parse_args()


def load_issues(path: Path) -> List[Dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in input file: {path}: {exc}") from exc

    if not isinstance(data, list):
        raise SystemExit("Input JSON must be an array of issues")

    normalized: List[Dict[str, Any]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        if not item.get("id") or not item.get("title"):
            continue
        normalized.append(item)
    return normalized


def to_jira_payload(issue: Dict[str, Any], project_key: str, label: str) -> Dict[str, Any]:
    beads_id = str(issue.get("id", "")).strip()
    title = str(issue.get("title", "")).strip()
    description = str(issue.get("description", "")).strip()
    status = str(issue.get("status", "open")).strip()
    priority = issue.get("priority", 2)
    issue_type = str(issue.get("issue_type", "task")).strip().lower()
    jira_issue_type = "Epic" if issue_type == "epic" else "Task"

    trace = f"beads_id: {beads_id}"
    summary = title[:255] if title else f"Beads issue {beads_id}"

    body = {
        "beads_id": beads_id,
        "action": "upsert",
        "jira": {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "issuetype": {"name": jira_issue_type},
                "labels": [label],
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": trace}],
                        },
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description or "(no description provided)",
                                }
                            ],
                        },
                    ],
                },
            }
        },
        "meta": {
            "status": status,
            "priority": priority,
            "issue_type": issue_type,
        },
    }
    return body


def dump_output(output_path: str, payload: Dict[str, Any]) -> None:
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if output_path == "-":
        sys.stdout.write(text)
        return
    Path(output_path).write_text(text, encoding="utf-8")


def filter_by_ids(issues: List[Dict[str, Any]], only_ids: str) -> List[Dict[str, Any]]:
    raw = [x.strip() for x in only_ids.split(",") if x.strip()]
    if not raw:
        return issues
    allowed = set(raw)
    return [issue for issue in issues if str(issue.get("id", "")).strip() in allowed]


def filter_by_epic_scope(issues: List[Dict[str, Any]], epic_id: str) -> List[Dict[str, Any]]:
    epic = epic_id.strip()
    if not epic:
        return issues
    prefix = epic + "."
    return [
        issue
        for issue in issues
        if str(issue.get("id", "")).strip() == epic
        or str(issue.get("id", "")).strip().startswith(prefix)
    ]


def main() -> int:
    args = parse_args()
    issues = load_issues(Path(args.input))
    issues = filter_by_ids(issues, args.only_ids)
    issues = filter_by_epic_scope(issues, args.epic_id)
    if args.max > 0:
        issues = issues[: args.max]

    payload = {
        "dry_run": bool(args.dry_run),
        "project_key": args.project_key,
        "label": args.label,
        "count": len(issues),
        "items": [to_jira_payload(i, args.project_key, args.label) for i in issues],
    }

    dump_output(args.output, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
