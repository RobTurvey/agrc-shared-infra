#!/usr/bin/env python3
"""Unit tests for beads_jira_sync scripts.

Run:
  python3 .agents/skills/beads_jira_sync/scripts/test_beads_jira_sync.py
"""

from __future__ import annotations

import importlib.util
import json
import tempfile
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
GEN = load_module(ROOT / "generate_sync_payload.py", "generate_sync_payload")


class GenerateSyncPayloadTests(unittest.TestCase):
    def test_filter_by_ids(self):
        issues = [
            {"id": "agrc-1", "title": "One"},
            {"id": "agrc-2", "title": "Two"},
            {"id": "agrc-3", "title": "Three"},
        ]
        filtered = GEN.filter_by_ids(issues, "agrc-2,agrc-3")
        self.assertEqual([i["id"] for i in filtered], ["agrc-2", "agrc-3"])

    def test_to_jira_payload_contains_traceability(self):
        issue = {
            "id": "agrc-auf.3",
            "title": "Daily sync",
            "description": "Sync bead tasks",
            "status": "in_progress",
            "priority": 1,
        }
        payload = GEN.to_jira_payload(issue, "DEV", "from-beads")
        self.assertEqual(payload["beads_id"], "agrc-auf.3")
        self.assertEqual(payload["jira"]["fields"]["project"]["key"], "DEV")
        self.assertIn("from-beads", payload["jira"]["fields"]["labels"])

    def test_to_jira_payload_epic_maps_to_epic_issue_type(self):
        issue = {
            "id": "agrc-auf",
            "title": "Continuous System and Process Improvements",
            "description": "Epic sample",
            "issue_type": "epic",
        }
        payload = GEN.to_jira_payload(issue, "DEV", "from-beads")
        self.assertEqual(payload["jira"]["fields"]["issuetype"]["name"], "Epic")

    def test_filter_by_epic_scope_includes_epic_and_children(self):
        issues = [
            {"id": "agrc-auf", "title": "Epic"},
            {"id": "agrc-auf.1", "title": "Child 1"},
            {"id": "agrc-auf.3", "title": "Child 3"},
            {"id": "agrc-other.1", "title": "Other"},
        ]
        filtered = GEN.filter_by_epic_scope(issues, "agrc-auf")
        self.assertEqual(
            [i["id"] for i in filtered],
            ["agrc-auf", "agrc-auf.1", "agrc-auf.3"],
        )

    def test_load_issues_array_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.json"
            p.write_text(json.dumps({"id": "x"}), encoding="utf-8")
            with self.assertRaises(SystemExit):
                GEN.load_issues(p)


if __name__ == "__main__":
    unittest.main(verbosity=2)
