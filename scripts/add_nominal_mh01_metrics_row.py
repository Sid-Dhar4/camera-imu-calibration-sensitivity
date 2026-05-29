#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path

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
    match = re.search(r"Duration:\\s+([0-9.]+)s", text)
    if not match:
        return None
    return float(match.group(1))


def read_existing_rows(metrics_path: Path) -> list[dict]:
    if not metrics_path.exists():
        return []
    with metrics_path.open(newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def main() -> int:
    run_id = "openvins_MH01_nominal_full_000"
    metrics_path = Path("results/metrics.csv")
    evo_summary_path = Path("results/evo") / run_id / "evo_summary.json"
    coverage_path = Path("results/logs/nominal") / run_id / "full_nominal_coverage_summary.txt"
    bag_info_path = Path("results/logs/setup/MH_01_easy_ros2_bag_info.txt")

    evo = json.loads(evo_summary_path.read_text())
    coverage = parse_key_value_file(coverage_path)
    bag_duration_s = parse_bag_duration(bag_info_path)

    estimated_duration_s = float(coverage["estimated_duration_s"])
    completion_rate = ""
    if bag_duration_s and bag_duration_s > 0:
        completion_rate = estimated_duration_s / bag_duration_s

    row = {
        "run_id": run_id,
        "sequence": "MH_01_easy",
        "backend": "openvins",
        "perturb_type": "nominal",
        "perturb_axis": "none",
        "perturb_magnitude": "0",
        "perturb_units": "none",
        "config_path": f"results/configs_used/{run_id}/estimator_config_full_safe.yaml",
        "trajectory_path": f"results/trajectories/nominal/{run_id}/openvins_estimate.tum",
        "status": "success",
        "ate_rmse_m": "{:.6f}".format(evo["ate_rmse_m"]),
        "rpe_trans_rmse_m": "{:.6f}".format(evo["rpe_trans_rmse_m"]),
        "rpe_rot_rmse_deg": "{:.6f}".format(evo["rpe_rot_rmse_deg"]),
        "runtime_s": "",
        "estimated_duration_s": "{:.6f}".format(estimated_duration_s),
        "completion_rate": "{:.6f}".format(completion_rate) if completion_rate != "" else "",
        "failure_reason": "",
        "notes": "Full nominal MH01 OpenVINS run; SE3 alignment no scale; RPE delta 20 frames.",
    }

    rows = read_existing_rows(metrics_path)
    rows = [r for r in rows if r.get("run_id") != run_id]
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
