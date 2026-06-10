#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path

REQUIRED_FALSE_KEYS = [
    "calib_cam_extrinsics",
    "calib_cam_intrinsics",
    "calib_cam_timeoffset",
]


def read_flag(text: str, key: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(key + ":"):
            return stripped
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify reported OpenVINS runs use frozen camera calibration flags.")
    parser.add_argument("--metrics", default="results/metrics.csv")
    args = parser.parse_args()

    rows = list(csv.DictReader(open(args.metrics)))
    failures = []

    for row in rows:
        if row["backend"] != "openvins" or row["status"] != "success":
            continue
        cfg = Path(row["config_path"])
        if not cfg.exists():
            failures.append((row["run_id"], str(cfg), "missing config"))
            continue
        text = cfg.read_text()
        for key in REQUIRED_FALSE_KEYS:
            flag = read_flag(text, key)
            if flag is None:
                failures.append((row["run_id"], str(cfg), f"{key} missing"))
            elif ": false" not in flag:
                failures.append((row["run_id"], str(cfg), flag))

    print(f"checked_reported_runs: {len(rows)}")
    print(f"freeze_flag_failures: {len(failures)}")
    for failure in failures:
        print("FAIL:", failure)

    if failures:
        return 1
    print("OK: all reported OpenVINS success configs freeze camera calibration flags")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
