#!/usr/bin/env python3
"""Unit tests for sync_all_beads_to_jira helpers.

Run:
  python3 .agents/skills/beads_jira_sync/scripts/test_sync_all_beads_jira.py
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


ROOT = Path(__file__).resolve().parent
SYNC_ALL = load_module(ROOT / "sync_all_beads_to_jira.py", "sync_all_beads_to_jira")


class SyncAllScopeTests(unittest.TestCase):
    def test_filter_scope_by_epic_and_sort(self):
        issues = [
            {"id": "agrc-auf.3", "title": "child-3", "status": "open"},
            {"id": "agrc-auf", "title": "epic", "status": "open"},
            {"id": "agrc-auf.10", "title": "child-10", "status": "open"},
            {"id": "agrc-other.1", "title": "other", "status": "open"},
        ]
        scoped = SYNC_ALL.filter_scope(issues, only_ids="", epic_id="agrc-auf", include_closed=False)
        self.assertEqual([i["id"] for i in scoped], ["agrc-auf", "agrc-auf.10", "agrc-auf.3"])

    def test_filter_scope_excludes_closed_by_default(self):
        issues = [
            {"id": "a-1", "title": "open", "status": "open"},
            {"id": "a-2", "title": "closed", "status": "closed"},
        ]
        scoped = SYNC_ALL.filter_scope(issues, only_ids="", epic_id="", include_closed=False)
        self.assertEqual([i["id"] for i in scoped], ["a-1"])

    def test_build_targets_resume_skips_completed(self):
        scoped = [
            {"id": "agrc-1", "title": "one"},
            {"id": "agrc-2", "title": "two"},
            {"id": "agrc-3", "title": "three"},
        ]
        state = {
            "completed": {
                "agrc-1": {"at": "2026-03-21T00:00:00Z"},
                "agrc-3": {"at": "2026-03-21T00:00:00Z"},
            },
            "failed": {
                "agrc-2": {"at": "2026-03-21T00:00:00Z", "attempts": 1},
            },
        }
        targets = SYNC_ALL.build_targets(scoped, state, restart=False)
        self.assertEqual([i["id"] for i in targets], ["agrc-2"])

    def test_build_targets_restart_replays_all(self):
        scoped = [
            {"id": "agrc-1", "title": "one"},
            {"id": "agrc-2", "title": "two"},
        ]
        state = {"completed": {"agrc-1": {"at": "x"}}}
        targets = SYNC_ALL.build_targets(scoped, state, restart=True)
        self.assertEqual([i["id"] for i in targets], ["agrc-1", "agrc-2"])


if __name__ == "__main__":
    unittest.main(verbosity=2)