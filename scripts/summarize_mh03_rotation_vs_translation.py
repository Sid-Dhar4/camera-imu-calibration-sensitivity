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
    raise ValueError(f"missing row for {sequence} {perturb_type} {axis} {magnitude}")


def build_summary(rows: list[dict]) -> list[dict]:
    specs = [
        ("nominal", "nominal", "none", "0"),
        ("rotation_z_2deg", "rotation", "z", "2.0"),
        ("rotation_z_5deg", "rotation", "z", "5.0"),
        ("translation_y_5cm", "translation", "y", "5.0"),
    ]
    summary = []
    for label, perturb_type, axis, magnitude in specs:
        row = find_row(rows, "MH_03_medium", perturb_type, axis, magnitude)
        summary.append(
            {
                "label": label,
                "perturb_type": row["perturb_type"],
                "axis": row["perturb_axis"],
                "magnitude": row["perturb_magnitude"],
                "units": row["perturb_units"],
                "ate_rmse_m": float(row["ate_rmse_m"]),
                "rpe_trans_rmse_m": float(row["rpe_trans_rmse_m"]),
                "rpe_rot_rmse_deg": float(row["rpe_rot_rmse_deg"]),
                "completion_rate": float(row["completion_rate"]),
            }
        )
    nominal_ate = summary[0]["ate_rmse_m"]
    for row in summary:
        row["ate_increase_x"] = row["ate_rmse_m"] / nominal_ate
    return summary


def write_table(summary: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)


def write_plot(summary: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 4))
    plt.bar([r["label"] for r in summary], [r["ate_rmse_m"] for r in summary])
    plt.yscale("log")
    plt.ylabel("ATE RMSE (m, log scale)")
    plt.title("MH_03_medium rotation vs translation calibration sensitivity")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=180)


def write_report(summary: list[dict], path: Path) -> None:
    nominal, rot2, rot5, trans5 = summary
    report = f"""# MH_03_medium Rotation-vs-Translation Error Budget

## Purpose

This report compares z-axis camera-IMU rotation perturbations against y-axis camera-IMU translation perturbation on EuRoC `MH_03_medium`.

## Summary

| Case | ATE RMSE (m) | Increase vs nominal | RPE trans RMSE (m) | RPE rot RMSE (deg) |
|---|---:|---:|---:|---:|
| nominal | {nominal["ate_rmse_m"]:.6f} | {nominal["ate_increase_x"]:.2f}x | {nominal["rpe_trans_rmse_m"]:.6f} | {nominal["rpe_rot_rmse_deg"]:.6f} |
| rotation-z 2deg | {rot2["ate_rmse_m"]:.6f} | {rot2["ate_increase_x"]:.2f}x | {rot2["rpe_trans_rmse_m"]:.6f} | {rot2["rpe_rot_rmse_deg"]:.6f} |
| rotation-z 5deg | {rot5["ate_rmse_m"]:.6f} | {rot5["ate_increase_x"]:.2f}x | {rot5["rpe_trans_rmse_m"]:.6f} | {rot5["rpe_rot_rmse_deg"]:.6f} |
| translation-y 5cm | {trans5["ate_rmse_m"]:.6f} | {trans5["ate_increase_x"]:.2f}x | {trans5["rpe_trans_rmse_m"]:.6f} | {trans5["rpe_rot_rmse_deg"]:.6f} |

## Interpretation

On `MH_03_medium`, the 5 cm y-axis translation perturbation stays close to nominal ATE RMSE: `{nominal["ate_rmse_m"]:.6f} m` nominal versus `{trans5["ate_rmse_m"]:.6f} m` perturbed.

The z-axis rotation perturbations are more damaging: 2 degrees increases ATE by `{rot2["ate_increase_x"]:.2f}x`, while 5 degrees causes severe trajectory divergence with a `{rot5["ate_increase_x"]:.2f}x` ATE increase.

This supports the current error-budget pattern: for the tested axes and magnitudes, z-axis camera-IMU rotation error is much more harmful than y-axis camera-IMU translation error.

## Artifacts

- Table: `results/tables/mh03_rotation_vs_translation_error_budget.csv`
- Plot: `results/plots/mh03_rotation_vs_translation_ate_rmse.png`
- Source metrics: `results/metrics.csv`

## Caution

This is a measured result for OpenVINS on one EuRoC sequence with frozen camera calibration. It should not be generalized to all axes, all datasets, or all VIO systems.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize MH03 rotation-vs-translation calibration sensitivity.")
    parser.add_argument("--metrics", default="results/metrics.csv")
    parser.add_argument("--table", default="results/tables/mh03_rotation_vs_translation_error_budget.csv")
    parser.add_argument("--plot", default="results/plots/mh03_rotation_vs_translation_ate_rmse.png")
    parser.add_argument("--report", default="reports/mh03_rotation_vs_translation_error_budget.md")
    args = parser.parse_args()

    summary = build_summary(read_metrics(Path(args.metrics)))
    write_table(summary, Path(args.table))
    write_plot(summary, Path(args.plot))
    write_report(summary, Path(args.report))
    print(f"wrote {args.table}")
    print(f"wrote {args.plot}")
    print(f"wrote {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
