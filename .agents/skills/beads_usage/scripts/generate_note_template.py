import argparse


def build_note(done: str, files: str, validation: str, risks: str, next_step: str) -> str:
    return (
        f"- What was done: {done}\n"
        f"- Files changed: {files}\n"
        f"- Validation run: {validation}\n"
        f"- Risks/blockers: {risks}\n"
        f"- Next step: {next_step}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate mandatory Beads note checklist text")
    parser.add_argument("--done", required=True, help="Summary of implemented work")
    parser.add_argument("--files", required=True, help="Comma-separated file paths")
    parser.add_argument("--validation", required=True, help="Checks and results")
    parser.add_argument("--risks", default="None", help="Risks or blockers")
    parser.add_argument("--next-step", default="None", help="Next step if any")
    args = parser.parse_args()

    print(
        build_note(
            done=args.done.strip(),
            files=args.files.strip(),
            validation=args.validation.strip(),
            risks=args.risks.strip(),
            next_step=args.next_step.strip(),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

