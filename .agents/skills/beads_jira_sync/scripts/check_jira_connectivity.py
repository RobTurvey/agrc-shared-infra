#!/usr/bin/env python3
"""Check Jira API connectivity using env-based basic auth.

This script performs a safe GET to /rest/api/3/myself and exits non-zero on failure.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check Jira REST API connectivity with env credentials"
    )
    parser.add_argument(
        "--base-url",
        default="",
        help="Jira base URL override (default: JIRA_BASE_URL or repo default)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=15.0,
        help="HTTP timeout in seconds (default: 15)",
    )
    return parser.parse_args()


def getenv(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def resolve_token() -> str:
    token = getenv("JIRA_API_TOKEN")
    if token:
        return token
    # Fallback noted in local docs
    return getenv("AGRC_BEADS_SYNC")


def main() -> int:
    args = parse_args()

    base_url = args.base_url.strip() or getenv("JIRA_BASE_URL") or "https://agentrealcoin.atlassian.net"
    email = getenv("JIRA_EMAIL")
    token = resolve_token()

    missing = []
    if not email:
        missing.append("JIRA_EMAIL")
    if not token:
        missing.append("JIRA_API_TOKEN (or AGRC_BEADS_SYNC fallback)")

    if missing:
        sys.stderr.write("Missing required env vars: " + ", ".join(missing) + "\n")
        return 2

    if not base_url.startswith("http"):
        sys.stderr.write("JIRA_BASE_URL must be absolute (https://...)\n")
        return 2

    url = base_url.rstrip("/") + "/rest/api/3/myself"
    creds = f"{email}:{token}".encode("utf-8")
    auth = base64.b64encode(creds).decode("ascii")
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Basic {auth}",
            "Accept": "application/json",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            data = json.loads(raw)
    except urllib.error.HTTPError as exc:
        sys.stderr.write(f"Jira connectivity failed: HTTP {exc.code}\n")
        return 1
    except urllib.error.URLError as exc:
        sys.stderr.write(f"Jira connectivity failed: {exc.reason}\n")
        return 1
    except json.JSONDecodeError:
        sys.stderr.write("Jira connectivity failed: non-JSON response\n")
        return 1

    account_id = str(data.get("accountId", ""))
    display_name = str(data.get("displayName", ""))
    print(
        json.dumps(
            {
                "ok": True,
                "endpoint": "/rest/api/3/myself",
                "accountId": account_id,
                "displayName": display_name,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
