#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def read_metrics(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def find_row(rows: list[dict], sequence: str, perturb_type: str, axis: str, magnitude: str) -> dict:
    for row in rows:
        if (
            row["sequence"] == sequence
            and row["perturb_type"] == perturb_type
            and row["perturb_axis"] == axis
            and row["perturb_magnitude"] == magnitude
        ):
            return row
    raise ValueError(f"missing row: {sequence} {perturb_type} {axis} {magnitude}")


def build_summary(rows: list[dict]) -> list[dict]:
    sequence_pairs = [
        ("MH_01_easy", "openvins_MH01_nominal_full_000", "openvins_MH01_rot_z_5deg_full_000"),
        ("MH_03_medium", "openvins_MH03_nominal_full_000", "openvins_MH03_rot_z_5deg_full_000"),
    ]

    out = []
    for sequence, nominal_run_id, rot5_run_id in sequence_pairs:
        nominal = next(r for r in rows if r["run_id"] == nominal_run_id)
        rot5 = next(r for r in rows if r["run_id"] == rot5_run_id)

        nominal_ate = float(nominal["ate_rmse_m"])
        rot5_ate = float(rot5["ate_rmse_m"])

        out.append({
            "sequence": sequence,
            "nominal_run_id": nominal_run_id,
            "rotation_z_5deg_run_id": rot5_run_id,
            "nominal_ate_rmse_m": nominal_ate,
            "rotation_z_5deg_ate_rmse_m": rot5_ate,
            "ate_increase_x": rot5_ate / nominal_ate,
            "nominal_rpe_trans_rmse_m": float(nominal["rpe_trans_rmse_m"]),
            "rotation_z_5deg_rpe_trans_rmse_m": float(rot5["rpe_trans_rmse_m"]),
            "nominal_rpe_rot_rmse_deg": float(nominal["rpe_rot_rmse_deg"]),
            "rotation_z_5deg_rpe_rot_rmse_deg": float(rot5["rpe_rot_rmse_deg"]),
            "nominal_completion_rate": float(nominal["completion_rate"]),
            "rotation_z_5deg_completion_rate": float(rot5["completion_rate"]),
        })

    return out


def write_table(summary: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "sequence",
        "nominal_run_id",
        "rotation_z_5deg_run_id",
        "nominal_ate_rmse_m",
        "rotation_z_5deg_ate_rmse_m",
        "ate_increase_x",
        "nominal_rpe_trans_rmse_m",
        "rotation_z_5deg_rpe_trans_rmse_m",
        "nominal_rpe_rot_rmse_deg",
        "rotation_z_5deg_rpe_rot_rmse_deg",
        "nominal_completion_rate",
        "rotation_z_5deg_completion_rate",
    ]
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary)


def write_plot(summary: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    labels = []
    values = []
    for row in summary:
        labels.extend([f"{row['sequence']} nominal", f"{row['sequence']} rot-z 5deg"])
        values.extend([row["nominal_ate_rmse_m"], row["rotation_z_5deg_ate_rmse_m"]])

    plt.figure(figsize=(9, 5))
    plt.bar(labels, values)
    plt.yscale("log")
    plt.ylabel("ATE RMSE (m), log scale")
    plt.title("Rotation-z 5deg calibration sensitivity across EuRoC sequences")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def write_report(summary: list[dict], table_path: Path, plot_path: Path, report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    mh01 = next(r for r in summary if r["sequence"] == "MH_01_easy")
    mh03 = next(r for r in summary if r["sequence"] == "MH_03_medium")

    report = f"""# Multi-sequence Rotation-z 5 Degree Sensitivity

## Purpose

This report compares the effect of a 5 degree camera-IMU z-axis rotation perturbation on two EuRoC MAV sequences.

## Summary

| Sequence | Nominal ATE RMSE (m) | Rotation-z 5deg ATE RMSE (m) | Increase |
|---|---:|---:|---:|
| MH_01_easy | {mh01['nominal_ate_rmse_m']:.6f} | {mh01['rotation_z_5deg_ate_rmse_m']:.6f} | {mh01['ate_increase_x']:.2f}x |
| MH_03_medium | {mh03['nominal_ate_rmse_m']:.6f} | {mh03['rotation_z_5deg_ate_rmse_m']:.6f} | {mh03['ate_increase_x']:.2f}x |

## Key observation

The 5 degree z-axis camera-IMU rotation perturbation degrades both sequences, but the effect is much larger on `MH_03_medium`.

On `MH_01_easy`, ATE RMSE increases from `{mh01['nominal_ate_rmse_m']:.6f} m` to `{mh01['rotation_z_5deg_ate_rmse_m']:.6f} m`.

On `MH_03_medium`, ATE RMSE increases from `{mh03['nominal_ate_rmse_m']:.6f} m` to `{mh03['rotation_z_5deg_ate_rmse_m']:.6f} m`, indicating severe trajectory divergence despite the estimator producing an output trajectory.

## Artifacts

- Table: `{table_path}`
- Plot: `{plot_path}`
- Source metrics: `results/metrics.csv`

## Caution

This is a measured result for OpenVINS on two EuRoC machine-hall sequences with frozen camera calibration. It should not yet be generalized to all datasets, all motion profiles, or all VIO systems.
"""
    report_path.write_text(report)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize multi-sequence rotation-z 5 degree sensitivity.")
    parser.add_argument("--metrics", default="results/metrics.csv", type=Path)
    parser.add_argument("--table", default="results/tables/mh01_mh03_rotation_z_5deg_summary.csv", type=Path)
    parser.add_argument("--plot", default="results/plots/mh01_mh03_rotation_z_5deg_ate_rmse.png", type=Path)
    parser.add_argument("--report", default="reports/mh01_mh03_rotation_z_5deg_summary.md", type=Path)
    args = parser.parse_args()

    rows = read_metrics(args.metrics)
    summary = build_summary(rows)
    write_table(summary, args.table)
    write_plot(summary, args.plot)
    write_report(summary, args.table, args.plot, args.report)

    print(f"wrote {args.table}")
    print(f"wrote {args.plot}")
    print(f"wrote {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
