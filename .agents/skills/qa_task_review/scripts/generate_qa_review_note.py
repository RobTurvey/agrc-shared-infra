import argparse


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a QA task review note skeleton")
    parser.add_argument("--decision", choices=["PASS", "NITS", "FAIL"], required=True)
    parser.add_argument("--scope", required=True)
    parser.add_argument("--ac", action="append", default=[], help="Acceptance criterion mapping line (repeatable)")
    parser.add_argument("--finding", action="append", default=[], help="Finding line with severity and evidence")
    parser.add_argument("--checks", action="append", default=[], help="Check executed (repeatable)")
    parser.add_argument("--runtime", choices=["container-beads", "local-lite"], required=True)
    parser.add_argument("--follow-up", default="None")
    args = parser.parse_args()

    print(f"- Decision: {args.decision}")
    print(f"- Scope reviewed: {args.scope}")
    print("- Acceptance criteria mapping:")
    if args.ac:
        for item in args.ac:
            print(f"  - {item}")
    else:
        print("  - None provided")

    print("- Findings:")
    if args.finding:
        for item in args.finding:
            print(f"  - {item}")
    else:
        print("  - None")

    print("- Checks run:")
    if args.checks:
        for item in args.checks:
            print(f"  - {item}")
    else:
        print("  - make agent-qa-check")

    print("- Runtime routing:")
    if args.runtime == "container-beads":
        print("  - Append to issue: bd update <id> --append-notes \"...\" --json")
    else:
        print("  - Update PR_DESCRIPTION.md with findings and evidence")

    print(f"- Follow-up issue (if FAIL/high): {args.follow_up}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
