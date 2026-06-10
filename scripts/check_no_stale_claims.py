#!/usr/bin/env python3
from pathlib import Path

FORBIDDEN = {
    "old_mh01_nominal_baseline": "0.139204",
    "old_mh01_rot5_increase_14_83x": "14.83x",
    "old_mh01_rot5_increase_14_834": "14.834",
    "timestamp_planned_not_reported": "Timestamp perturbation is planned but not reported here.",
    "optional_timestamp_extension": "- optional timestamp offset perturbation",
    "rotation_translation_only_benchmark_table": "| Perturbations | camera-IMU z-axis rotation; camera-IMU y-axis translation |",
    "rotation_translation_only_limitation": "Current reported perturbations cover z-axis camera-IMU rotation and y-axis camera-IMU translation only.",
    "old_error_budget_plan": "- error-budget summary comparing rotation and translation sensitivity",
}

SEARCH_ROOTS = [Path("README.md"), Path("docs"), Path("reports"), Path("results/tables")]

def iter_text_files():
    for root in SEARCH_ROOTS:
        if root.is_file():
            yield root
        elif root.is_dir():
            for path in root.rglob("*"):
                if path.is_file() and path.suffix.lower() in {".md", ".txt", ".csv"}:
                    yield path

def main() -> int:
    failures = []
    for path in iter_text_files():
        text = path.read_text(errors="replace")
        for label, needle in FORBIDDEN.items():
            if needle in text:
                failures.append((label, str(path), needle))
    if failures:
        print("ERROR: stale claims found")
        for label, path, needle in failures:
            print(f"{label}: {path}: {needle}")
        return 1
    print("OK: no stale benchmark claims found")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
