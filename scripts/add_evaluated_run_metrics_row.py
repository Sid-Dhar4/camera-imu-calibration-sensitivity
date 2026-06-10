#!/usr/bin/env python3
import argparse
import csv
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from metrics.schema import REQUIRED_COLUMNS


def parse_key_value_file(path: Path) -> dict:
    out = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip()
    return out


def parse_bag_duration(path: Path) -> float | None:
    if not path.exists():
        return None
    text = path.read_text()
    match = re.search(r"Duration:\s+([0-9.]+)s", text)
    if not match:
        return None
    return float(match.group(1))


def read_existing_rows(metrics_path: Path) -> list[dict]:
    if not metrics_path.exists():
        return []
    with metrics_path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    parser = argparse.ArgumentParser(description="Add or replace one evaluated run row in results/metrics.csv.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--sequence", required=True)
    parser.add_argument("--backend", default="openvins")
    parser.add_argument("--perturb-type", required=True)
    parser.add_argument("--perturb-axis", required=True)
    parser.add_argument("--perturb-magnitude", required=True)
    parser.add_argument("--perturb-units", required=True)
    parser.add_argument("--config-path", required=True)
    parser.add_argument("--trajectory-path", required=True)
    parser.add_argument("--evo-summary", required=True, type=Path)
    parser.add_argument("--coverage-summary", required=True, type=Path)
    parser.add_argument("--notes", required=True)
    args = parser.parse_args()

    metrics_path = Path("results/metrics.csv")
    bag_info_path = Path("results/logs/setup") / f"{args.sequence}_ros2_bag_info.txt"

    evo = json.loads(args.evo_summary.read_text())
    coverage = parse_key_value_file(args.coverage_summary)
    bag_duration_s = parse_bag_duration(bag_info_path)

    estimated_duration_s = float(coverage["estimated_duration_s"])
    completion_rate = ""
    if bag_duration_s and bag_duration_s > 0:
        completion_rate = estimated_duration_s / bag_duration_s

    row = {
        "run_id": args.run_id,
        "sequence": args.sequence,
        "backend": args.backend,
        "perturb_type": args.perturb_type,
        "perturb_axis": args.perturb_axis,
        "perturb_magnitude": args.perturb_magnitude,
        "perturb_units": args.perturb_units,
        "config_path": args.config_path,
        "trajectory_path": args.trajectory_path,
        "status": "success",
        "ate_rmse_m": "{:.6f}".format(evo["ate_rmse_m"]),
        "rpe_trans_rmse_m": "{:.6f}".format(evo["rpe_trans_rmse_m"]),
        "rpe_rot_rmse_deg": "{:.6f}".format(evo["rpe_rot_rmse_deg"]),
        "runtime_s": "",
        "estimated_duration_s": "{:.6f}".format(estimated_duration_s),
        "completion_rate": "{:.6f}".format(completion_rate) if completion_rate != "" else "",
        "failure_reason": "",
        "notes": args.notes,
    }

    rows = read_existing_rows(metrics_path)
    rows = [r for r in rows if r.get("run_id") != args.run_id]
    rows.append(row)

    with metrics_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print("wrote metrics row:")
    for key in REQUIRED_COLUMNS:
        print(f"{key}: {row[key]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
