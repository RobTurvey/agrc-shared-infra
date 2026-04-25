import argparse
import json
import re
from pathlib import Path


def parse_logs(file_path: Path) -> dict:
    error_re = re.compile(r"ERROR[:\s]+(.+)")
    warn_re = re.compile(r"WARN[:\s]+(.+)")
    counts = {"error": 0, "warn": 0}
    samples = {"error": [], "warn": []}

    for line in file_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        e = error_re.search(line)
        w = warn_re.search(line)
        if e:
            counts["error"] += 1
            if len(samples["error"]) < 5:
                samples["error"].append(e.group(1))
        if w:
            counts["warn"] += 1
            if len(samples["warn"]) < 5:
                samples["warn"].append(w.group(1))

    return {"counts": counts, "samples": samples}


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse logs and emit grouped warning/error summary")
    parser.add_argument("--file", required=True, help="Path to .log or .txt file")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists() or not path.is_file():
        print(f"Input file not found: {path}")
        return 2

    result = parse_logs(path)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

