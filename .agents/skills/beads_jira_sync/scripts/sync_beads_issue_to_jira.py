#!/usr/bin/env python3
"""Sync a single Beads issue to Jira by beads_id marker.

Usage:
  python3 .agents/skills/beads_jira_sync/scripts/sync_beads_issue_to_jira.py --beads-id agrc-auf
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import time
import urllib.parse
import urllib.error
import urllib.request
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Sync one Beads issue into Jira (upsert by beads_id marker)")
    p.add_argument("--beads-id", required=True, help="Beads issue id, e.g. agrc-auf")
    p.add_argument("--project-key", default="DEV", help="Jira project key (default: DEV)")
    p.add_argument("--label", default="from-beads", help="Jira label marker (default: from-beads)")
    p.add_argument("--jira-type", default="", help="Override Jira issue type name (Epic|Task|Subtask)")
    p.add_argument("--parent-beads-id", default="", help="Parent Beads ID (used when creating Subtask)")
    p.add_argument("--parent-jira-key", default="", help="Parent Jira key (used when creating Subtask)")
    p.add_argument(
        "--cache-file",
        default=".agents/skills/beads_jira_sync/assets/jira_sync_map.json",
        help="Local cache mapping beads_id -> jira_key",
    )
    p.add_argument("--dry-run", action="store_true", help="Do not mutate Jira; print intended action")
    p.add_argument("--base-url", default="", help="Jira base url override")
    p.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout seconds")
    return p.parse_args()


def load_env_file(path: str = ".env") -> None:
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def adf(marker: str, description: str) -> dict:
    return {
        "type": "doc",
        "version": 1,
        "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": marker}]},
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": description or "(no description provided)"}],
            },
        ],
    }


def jira_request(base: str, method: str, path: str, headers: dict, body: dict | None, timeout: float) -> dict | None:
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(base.rstrip("/") + path, headers=headers, data=data, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
        return json.loads(raw) if raw else None


def load_cache(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "items": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"version": 1, "items": {}}
    if not isinstance(data, dict):
        return {"version": 1, "items": {}}
    items = data.get("items")
    if not isinstance(items, dict):
        data["items"] = {}
    return data


def save_cache(path: Path, cache: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def detect_issue_types(base: str, project_key: str, headers: dict, timeout: float) -> dict[str, dict]:
    proj = jira_request(base, "GET", f"/rest/api/3/project/{project_key}", headers, None, timeout) or {}
    project_id = proj.get("id")
    if not project_id:
        return {}
    types = jira_request(
        base,
        "GET",
        f"/rest/api/3/issuetype/project?projectId={project_id}",
        headers,
        None,
        timeout,
    ) or []
    out: dict[str, dict] = {}
    if isinstance(types, list):
        for t in types:
            name = str(t.get("name", "")).strip()
            if name:
                out[name.lower()] = t
    return out


def infer_jira_type_name(beads_issue: dict, override: str) -> str:
    if override.strip():
        return override.strip()
    src = str(beads_issue.get("issue_type", "")).strip().lower()
    if src == "epic":
        return "Epic"
    if src in {"subtask", "sub-task", "sub_task"}:
        return "Subtask"
    return "Task"


def main() -> int:
    args = parse_args()
    load_env_file()

    base = (args.base_url or os.getenv("JIRA_BASE_URL") or "https://agentrealcoin.atlassian.net").strip()
    email = os.getenv("JIRA_EMAIL", "").strip()
    token = os.getenv("JIRA_API_TOKEN", "").strip() or os.getenv("AGRC_BEADS_SYNC", "").strip()
    if not email or not token:
        raise SystemExit("Missing JIRA_EMAIL and/or JIRA_API_TOKEN (or AGRC_BEADS_SYNC)")

    issue = json.loads(subprocess.check_output(["bd", "show", args.beads_id, "--json"], text=True))[0]
    marker = f"beads_id: {issue['id']}"
    summary = issue["title"][:255]
    issue_type = infer_jira_type_name(issue, args.jira_type)

    auth = base64.b64encode(f"{email}:{token}".encode("utf-8")).decode("ascii")
    headers = {
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    available_types = detect_issue_types(base, args.project_key, headers, args.timeout)
    if issue_type.lower() not in available_types:
        raise SystemExit(
            f"Requested Jira type '{issue_type}' is not available in project {args.project_key}. "
            f"Available: {', '.join(sorted(t.get('name','') for t in available_types.values()))}"
        )

    cache_path = Path(args.cache_file)
    cache = load_cache(cache_path)
    cache_items = cache.setdefault("items", {})

    cached_key = ""
    entry = cache_items.get(args.beads_id)
    if isinstance(entry, dict):
        cached_key = str(entry.get("jira_key", "")).strip()

    if cached_key:
        try:
            jira_request(base, "GET", f"/rest/api/3/issue/{cached_key}?fields=summary", headers, None, args.timeout)
            issues = [{"key": cached_key}]
        except urllib.error.HTTPError:
            issues = []
    else:
        issues = []

    if not issues:
        jql = f'project = {args.project_key} AND labels = {args.label} AND text ~ "\\"{marker}\\"" ORDER BY updated DESC'
        query = urllib.parse.urlencode({"jql": jql, "maxResults": 5, "fields": "summary"})
        found = jira_request(base, "GET", f"/rest/api/3/search/jql?{query}", headers, None, args.timeout) or {}
        issues = found.get("issues", [])

    fields = {
        "summary": summary,
        "description": adf(marker, str(issue.get("description", ""))),
        "labels": [args.label],
    }

    if issues:
        key = issues[0]["key"]
        if args.dry_run:
            print(json.dumps({"mode": "would_update", "beads_id": args.beads_id, "jira_key": key}, ensure_ascii=False))
            return 0
        jira_request(base, "PUT", f"/rest/api/3/issue/{key}", headers, {"fields": fields}, args.timeout)
        cache_items[args.beads_id] = {
            "jira_key": key,
            "jira_type": issue_type,
            "updated_at": int(time.time()),
        }
        save_cache(cache_path, cache)
        print(json.dumps({"mode": "updated", "beads_id": args.beads_id, "jira_key": key}, ensure_ascii=False))
        return 0

    create_fields = {
        "project": {"key": args.project_key},
        "summary": summary,
        "issuetype": {"name": issue_type},
        "description": fields["description"],
        "labels": [args.label],
    }

    if issue_type.lower() == "subtask":
        parent_key = args.parent_jira_key.strip()
        if not parent_key and args.parent_beads_id.strip():
            parent_entry = cache_items.get(args.parent_beads_id.strip())
            if isinstance(parent_entry, dict):
                parent_key = str(parent_entry.get("jira_key", "")).strip()
        if not parent_key:
            raise SystemExit("Subtask requires --parent-jira-key or a cached --parent-beads-id mapping")
        create_fields["parent"] = {"key": parent_key}

    if args.dry_run:
        print(
            json.dumps(
                {
                    "mode": "would_create",
                    "beads_id": args.beads_id,
                    "jira_type": issue_type,
                    "fields_preview": {"summary": summary, "issuetype": issue_type},
                },
                ensure_ascii=False,
            )
        )
        return 0

    created = jira_request(base, "POST", "/rest/api/3/issue", headers, {"fields": create_fields}, args.timeout) or {}
    key = created.get("key")
    if key:
        cache_items[args.beads_id] = {
            "jira_key": key,
            "jira_type": issue_type,
            "updated_at": int(time.time()),
        }
        save_cache(cache_path, cache)
    print(json.dumps({"mode": "created", "beads_id": args.beads_id, "jira_key": key, "jira_type": issue_type}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
