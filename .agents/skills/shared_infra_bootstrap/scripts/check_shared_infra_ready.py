#!/usr/bin/env python3
"""Validate shared-infra baseline layout for submodule consumption."""

import argparse
from pathlib import Path
import sys

REQUIRED = [
    ".agents/skills",
    ".github/skills",
    ".agent/profiles",
    "templates",
    "scripts",
    "README.md",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check shared-infra baseline readiness.")
    parser.add_argument(
        "--root",
        default=".",
        help="Path to shared-infra repository root (default: current directory).",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    missing = []

    for rel in REQUIRED:
        target = root / rel
        if not target.exists():
            missing.append(rel)

    if missing:
        print("FAIL: missing required paths:")
        for item in missing:
            print(f"- {item}")
        return 1

    print("PASS: shared-infra baseline layout is present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
