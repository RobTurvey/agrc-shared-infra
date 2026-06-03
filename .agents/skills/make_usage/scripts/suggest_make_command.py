import argparse


SUGGESTIONS = {
    "runtime": "make agent-runtime-check",
    "init": "make agent-init ISSUE=<id> ACTOR=<agrc/copilot|agrc/codex|agrc/claude>",
    "qa": "make agent-qa-check",
    "checklist": "make agent-comment-checklist ISSUE=<id>",
    "append-note": "make agent-append-note ISSUE=<id> NOTE=\"...\"",
    "handoff": "make mem-handoff",
    "post-rebuild": "make post-rebuild-check",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest make command by workflow step")
    parser.add_argument("--step", required=True, help=f"One of: {', '.join(SUGGESTIONS.keys())}")
    args = parser.parse_args()

    step = args.step.strip().lower()
    if step not in SUGGESTIONS:
        print("Unknown step.")
        print(f"Valid steps: {', '.join(SUGGESTIONS.keys())}")
        return 1

    print(SUGGESTIONS[step])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
