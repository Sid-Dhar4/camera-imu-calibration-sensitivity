#!/usr/bin/env python3
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from metrics.schema import REQUIRED_COLUMNS, ALLOWED_STATUS, ALLOWED_PERTURB_TYPES


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/check_results_schema.py results/metrics.csv")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: file does not exist: {path}")
        return 1

    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames

        if header != REQUIRED_COLUMNS:
            print("ERROR: metrics.csv header does not match schema.")
            print("Expected:")
            print(REQUIRED_COLUMNS)
            print("Found:")
            print(header)
            return 1

        for i, row in enumerate(reader, start=2):
            status = row["status"].strip()
            perturb_type = row["perturb_type"].strip()

            if status and status not in ALLOWED_STATUS:
                print(f"ERROR: row {i} has invalid status: {status}")
                return 1

            if perturb_type and perturb_type not in ALLOWED_PERTURB_TYPES:
                print(f"ERROR: row {i} has invalid perturb_type: {perturb_type}")
                return 1

            if status and status != "success" and not row["failure_reason"].strip():
                print(f"ERROR: row {i} has status={status} but empty failure_reason")
                return 1

    print(f"OK: {path} matches metrics schema.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
