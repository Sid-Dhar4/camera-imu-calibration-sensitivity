#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path


FIELDS = [
    "run_id",
    "sequence",
    "backend",
    "perturb_type",
    "perturb_axis",
    "perturb_magnitude",
    "perturb_units",
    "status",
    "ate_rmse_m",
    "rpe_trans_rmse_m",
    "rpe_rot_rmse_deg",
    "completion_rate",
    "config_path",
    "config_exists",
    "trajectory_path",
    "trajectory_exists",
    "evo_summary_path",
    "evo_summary_exists",
    "included_reports",
]


def run_group(row: dict) -> str:
    return "nominal" if row["perturb_type"] == "nominal" else "perturbed"


def included_reports(row: dict) -> str:
    reports = []
    seq = row["sequence"]
    ptype = row["perturb_type"]
    axis = row["perturb_axis"]
    mag = row["perturb_magnitude"]

    if seq == "MH_01_easy":
        reports.append("reports/mh01_rotation_vs_translation_error_budget.md")
        if ptype in {"nominal", "rotation"}:
            reports.append("reports/mh01_rotation_z_sweep.md")

    if seq == "MH_03_medium" and (ptype == "nominal" or (ptype == "rotation" and axis == "z")):
        reports.append("reports/mh03_rotation_z_sensitivity.md")

    if (seq == "MH_01_easy" and (ptype == "nominal" or (ptype == "rotation" and axis == "z" and mag == "5.0"))) or (seq == "MH_03_medium" and (ptype == "nominal" or (ptype == "rotation" and axis == "z" and mag == "5.0"))):
        reports.append("reports/mh01_mh03_rotation_z_5deg_summary.md")

    return ";".join(dict.fromkeys(reports))


def manifest_row(row: dict) -> dict:
    group = run_group(row)
    run_id = row["run_id"]
    evo_summary_path = Path("results/evo") / group / run_id / "evo_summary.json"
    config_path = Path(row["config_path"])
    trajectory_path = Path(row["trajectory_path"])
    return {
        "run_id": run_id,
        "sequence": row["sequence"],
        "backend": row["backend"],
        "perturb_type": row["perturb_type"],
        "perturb_axis": row["perturb_axis"],
        "perturb_magnitude": row["perturb_magnitude"],
        "perturb_units": row["perturb_units"],
        "status": row["status"],
        "ate_rmse_m": row["ate_rmse_m"],
        "rpe_trans_rmse_m": row["rpe_trans_rmse_m"],
        "rpe_rot_rmse_deg": row["rpe_rot_rmse_deg"],
        "completion_rate": row["completion_rate"],
        "config_path": str(config_path),
        "config_exists": str(config_path.exists()).lower(),
        "trajectory_path": str(trajectory_path),
        "trajectory_exists": str(trajectory_path.exists()).lower(),
        "evo_summary_path": str(evo_summary_path),
        "evo_summary_exists": str(evo_summary_path.exists()).lower(),
        "included_reports": included_reports(row),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an auditable run manifest from results/metrics.csv.")
    parser.add_argument("--metrics", default="results/metrics.csv")
    parser.add_argument("--output", default="results/run_manifest.csv")
    args = parser.parse_args()

    metrics_path = Path(args.metrics)
    output_path = Path(args.output)
    with metrics_path.open(newline="") as f:
        rows = list(csv.DictReader(f))

    manifest = [manifest_row(row) for row in rows]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(manifest)

    print(f"wrote {output_path}")
    print(f"runs: {len(manifest)}")
    missing = [r["run_id"] for r in manifest if r["config_exists"] != "true" or r["trajectory_exists"] != "true"]
    if missing:
        print("warning: missing checked paths for runs: " + ", ".join(missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
