#!/usr/bin/env python3
import argparse
import csv
import re
from pathlib import Path


ARTIFACT_PATTERN = re.compile(r"`([^`]+)`")


def manifest_paths(path: Path) -> list[Path]:
    rows = list(csv.DictReader(path.open()))
    paths = []
    for row in rows:
        for key in ["config_path", "trajectory_path", "evo_summary_path"]:
            value = row.get(key, "").strip()
            if value:
                paths.append(Path(value))
        reports = row.get("included_reports", "").strip()
        if reports:
            for report in reports.split(";"):
                if report.strip():
                    paths.append(Path(report.strip()))
    return paths


def readme_artifact_paths(path: Path) -> list[Path]:
    paths = []
    in_artifacts = False
    for line in path.read_text().splitlines():
        if line.strip() == "## Primary artifacts":
            in_artifacts = True
            continue
        if in_artifacts and line.startswith("## "):
            break
        if in_artifacts:
            for match in ARTIFACT_PATTERN.findall(line):
                if match.startswith(("results/", "reports/", "docs/", "scripts/")):
                    paths.append(Path(match))
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Check that benchmark artifacts referenced by manifest and README exist.")
    parser.add_argument("--manifest", default="results/run_manifest.csv")
    parser.add_argument("--readme", default="README.md")
    args = parser.parse_args()

    paths = []
    paths.extend(manifest_paths(Path(args.manifest)))
    paths.extend(readme_artifact_paths(Path(args.readme)))
    unique = sorted(set(paths), key=str)

    missing = [p for p in unique if not p.exists()]
    print(f"checked_paths: {len(unique)}")
    print(f"missing_paths: {len(missing)}")
    for p in missing:
        print(f"MISSING: {p}")

    if missing:
        return 1
    print("OK: all referenced artifacts exist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
