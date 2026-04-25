#!/usr/bin/env python3
"""Manual batch sync of Beads issues to Jira with resume support.

This script is designed for on-demand execution (no scheduler required).
It persists progress so reruns continue from pending/failed work unless
`--restart-from-beginning` is supplied.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync Beads issues to Jira in batch with checkpoint/resume support"
    )
    parser.add_argument("--issues-file", default=".beads/issues.jsonl", help="Beads export file path")
    parser.add_argument("--refresh-export", action="store_true", help="Run `bd export` before reading issues")
    parser.add_argument("--epic-id", default="", help="Only include <epic-id> and <epic-id>.*")
    parser.add_argument("--only-ids", default="", help="Comma-separated issue IDs to include")
    parser.add_argument("--include-closed", action="store_true", help="Include closed issues")
    parser.add_argument("--apply", action="store_true", help="Execute Jira writes")
    parser.add_argument("--dry-run", action="store_true", help="Plan only; no Jira writes")
    parser.add_argument(
        "--restart-from-beginning",
        action="store_true",
        help="Ignore saved completion state and replay all scoped issues",
    )
    parser.add_argument(
        "--state-file",
        default=".agents/skills/beads_jira_sync/assets/sync_all_state.json",
        help="Checkpoint file for completed/failed issue IDs",
    )
    parser.add_argument(
        "--report-file",
        default=".agents/skills/beads_jira_sync/assets/sync_all_report.json",
        help="JSON report output path",
    )
    parser.add_argument("--project-key", default="DEV", help="Jira project key")
    parser.add_argument("--label", default="from-beads", help="Jira label marker")
    parser.add_argument("--base-url", default="", help="Jira base URL override")
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout for child sync script")
    parser.add_argument(
        "--cache-file",
        default=".agents/skills/beads_jira_sync/assets/jira_sync_map.json",
        help="Local cache mapping beads_id -> jira_key",
    )
    return parser.parse_args()


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def maybe_refresh_export(issues_file: Path, refresh: bool) -> None:
    if not refresh:
        return
    subprocess.check_call(["bd", "export", "-o", str(issues_file)])


def load_jsonl_issues(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"Issues file not found: {path}")
    items: list[dict] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not s:
            continue
        try:
            obj = json.loads(s)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and obj.get("id") and obj.get("title"):
            items.append(obj)
    return items


def filter_scope(issues: list[dict], only_ids: str, epic_id: str, include_closed: bool) -> list[dict]:
    selected = issues
    if not include_closed:
        selected = [i for i in selected if str(i.get("status", "")).lower() != "closed"]

    if only_ids.strip():
        allowed = {part.strip() for part in only_ids.split(",") if part.strip()}
        selected = [i for i in selected if str(i.get("id", "")).strip() in allowed]

    if epic_id.strip():
        epic = epic_id.strip()
        prefix = epic + "."
        selected = [
            i
            for i in selected
            if str(i.get("id", "")).strip() == epic
            or str(i.get("id", "")).strip().startswith(prefix)
        ]

    def sort_key(issue: dict) -> tuple[int, str]:
        issue_id = str(issue.get("id", "")).strip()
        return (issue_id.count("."), issue_id)

    return sorted(selected, key=sort_key)


def load_state(path: Path) -> dict:
    if not path.exists():
        return {
            "version": 1,
            "updated_at": now_iso(),
            "completed": {},
            "failed": {},
        }
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {
            "version": 1,
            "updated_at": now_iso(),
            "completed": {},
            "failed": {},
        }
    if not isinstance(data, dict):
        return {
            "version": 1,
            "updated_at": now_iso(),
            "completed": {},
            "failed": {},
        }
    data.setdefault("version", 1)
    data.setdefault("updated_at", now_iso())
    data.setdefault("completed", {})
    data.setdefault("failed", {})
    if not isinstance(data["completed"], dict):
        data["completed"] = {}
    if not isinstance(data["failed"], dict):
        data["failed"] = {}
    return data


def save_state(path: Path, state: dict) -> None:
    state["updated_at"] = now_iso()
    ensure_parent(path)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_targets(scoped_issues: list[dict], state: dict, restart: bool) -> list[dict]:
    if restart:
        return scoped_issues
    completed_ids = set(state.get("completed", {}).keys())
    return [issue for issue in scoped_issues if str(issue.get("id", "")) not in completed_ids]


def run_single_sync(args: argparse.Namespace, beads_id: str) -> tuple[int, dict | None, str]:
    cmd = [
        "python3",
        ".agents/skills/beads_jira_sync/scripts/sync_beads_issue_to_jira.py",
        "--beads-id",
        beads_id,
        "--project-key",
        args.project_key,
        "--label",
        args.label,
        "--cache-file",
        args.cache_file,
        "--timeout",
        str(args.timeout),
    ]
    if args.base_url.strip():
        cmd.extend(["--base-url", args.base_url.strip()])
    if args.dry_run or not args.apply:
        cmd.append("--dry-run")

    proc = subprocess.run(cmd, text=True, capture_output=True)
    payload = None
    out = (proc.stdout or "").strip()
    if out:
        lines = out.splitlines()
        for candidate in reversed(lines):
            candidate = candidate.strip()
            if not candidate:
                continue
            try:
                payload = json.loads(candidate)
                break
            except json.JSONDecodeError:
                continue

    err = (proc.stderr or "").strip()
    if proc.returncode != 0 and not err:
        err = out or "sync child process failed"
    return proc.returncode, payload, err


def main() -> int:
    args = parse_args()
    if args.apply and args.dry_run:
        raise SystemExit("Use only one mode: --apply or --dry-run")

    issues_file = Path(args.issues_file)
    state_file = Path(args.state_file)
    report_file = Path(args.report_file)

    started_at = time.time()
    start_iso = now_iso()

    maybe_refresh_export(issues_file, args.refresh_export)
    issues = load_jsonl_issues(issues_file)
    scoped = filter_scope(issues, args.only_ids, args.epic_id, args.include_closed)
    state = load_state(state_file)
    targets = build_targets(scoped, state, args.restart_from_beginning)

    results: list[dict] = []
    counts = {
        "scoped": len(scoped),
        "queued": len(targets),
        "created": 0,
        "updated": 0,
        "skipped": 0,
        "failed": 0,
        "would_create": 0,
        "would_update": 0,
    }

    failed_any = False
    mode = "apply" if args.apply else "dry-run"

    for issue in targets:
        beads_id = str(issue.get("id", "")).strip()
        if not beads_id:
            continue

        code, payload, err = run_single_sync(args, beads_id)
        if code == 0:
            sync_mode = str((payload or {}).get("mode", "ok"))
            entry = {
                "beads_id": beads_id,
                "status": "ok",
                "sync_mode": sync_mode,
                "jira_key": (payload or {}).get("jira_key"),
            }
            results.append(entry)

            if sync_mode == "created":
                counts["created"] += 1
            elif sync_mode == "updated":
                counts["updated"] += 1
            elif sync_mode == "would_create":
                counts["would_create"] += 1
            elif sync_mode == "would_update":
                counts["would_update"] += 1
            else:
                counts["skipped"] += 1

            if args.apply:
                state.setdefault("completed", {})[beads_id] = {
                    "at": now_iso(),
                    "mode": sync_mode,
                    "jira_key": (payload or {}).get("jira_key"),
                }
                state.setdefault("failed", {}).pop(beads_id, None)
                save_state(state_file, state)
            continue

        failed_any = True
        counts["failed"] += 1
        entry = {
            "beads_id": beads_id,
            "status": "failed",
            "error": err,
        }
        results.append(entry)
        if args.apply:
            old = state.setdefault("failed", {}).get(beads_id, {})
            attempts = int(old.get("attempts", 0)) + 1
            state.setdefault("failed", {})[beads_id] = {
                "at": now_iso(),
                "attempts": attempts,
                "error": err,
            }
            save_state(state_file, state)

    finished_at = time.time()
    report = {
        "started_at": start_iso,
        "finished_at": now_iso(),
        "duration_sec": round(finished_at - started_at, 3),
        "mode": mode,
        "scope": {
            "issues_file": str(issues_file),
            "epic_id": args.epic_id,
            "only_ids": args.only_ids,
            "include_closed": bool(args.include_closed),
            "restart_from_beginning": bool(args.restart_from_beginning),
        },
        "counts": counts,
        "results": results,
        "state_file": str(state_file),
    }
    ensure_parent(report_file)
    report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({"ok": not failed_any, "mode": mode, "report_file": str(report_file), "counts": counts}, ensure_ascii=False))
    return 1 if failed_any else 0


if __name__ == "__main__":
    raise SystemExit(main())