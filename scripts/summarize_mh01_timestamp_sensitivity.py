#!/usr/bin/env python3
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def read_metrics(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def find(rows: list[dict], run_id: str) -> dict:
    for row in rows:
        if row["run_id"] == run_id:
            return row
    raise ValueError(f"missing run: {run_id}")


def main() -> int:
    rows = read_metrics(Path("results/metrics.csv"))
    specs = [
        ("nominal", "openvins_MH01_nominal_full_000"),
        ("timestamp_10ms", "openvins_MH01_time_10ms_full_000"),
        ("translation_y_5cm", "openvins_MH01_trans_y_5cm_full_000"),
        ("rotation_z_5deg", "openvins_MH01_rot_z_5deg_full_000"),
    ]
    summary = []
    for label, run_id in specs:
        row = find(rows, run_id)
        summary.append({
            "label": label,
            "run_id": run_id,
            "perturb_type": row["perturb_type"],
            "axis": row["perturb_axis"],
            "magnitude": row["perturb_magnitude"],
            "units": row["perturb_units"],
            "ate_rmse_m": float(row["ate_rmse_m"]),
            "rpe_trans_rmse_m": float(row["rpe_trans_rmse_m"]),
            "rpe_rot_rmse_deg": float(row["rpe_rot_rmse_deg"]),
            "completion_rate": float(row["completion_rate"]),
        })

    nominal_ate = summary[0]["ate_rmse_m"]
    for row in summary:
        row["ate_increase_x"] = row["ate_rmse_m"] / nominal_ate

    table = Path("results/tables/mh01_timestamp_sensitivity_summary.csv")
    table.parent.mkdir(parents=True, exist_ok=True)
    with table.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)

    plot = Path("results/plots/mh01_timestamp_sensitivity_ate_rmse.png")
    plot.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 4))
    plt.bar([r["label"] for r in summary], [r["ate_rmse_m"] for r in summary])
    plt.yscale("log")
    plt.ylabel("ATE RMSE (m, log scale)")
    plt.title("MH_01_easy timestamp vs extrinsic perturbations")
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    plt.savefig(plot, dpi=180)

    nominal, timestamp, translation, rotation = summary
    report = f"""# MH_01_easy Timestamp Sensitivity

## Purpose

This report adds a temporal calibration perturbation to the existing extrinsic calibration sensitivity benchmark.

## Summary

| Case | ATE RMSE (m) | Increase vs nominal | RPE trans RMSE (m) | RPE rot RMSE (deg) |
|---|---:|---:|---:|---:|
| nominal | {nominal["ate_rmse_m"]:.6f} | {nominal["ate_increase_x"]:.2f}x | {nominal["rpe_trans_rmse_m"]:.6f} | {nominal["rpe_rot_rmse_deg"]:.6f} |
| timestamp 10ms | {timestamp["ate_rmse_m"]:.6f} | {timestamp["ate_increase_x"]:.2f}x | {timestamp["rpe_trans_rmse_m"]:.6f} | {timestamp["rpe_rot_rmse_deg"]:.6f} |
| translation-y 5cm | {translation["ate_rmse_m"]:.6f} | {translation["ate_increase_x"]:.2f}x | {translation["rpe_trans_rmse_m"]:.6f} | {translation["rpe_rot_rmse_deg"]:.6f} |
| rotation-z 5deg | {rotation["ate_rmse_m"]:.6f} | {rotation["ate_increase_x"]:.2f}x | {rotation["rpe_trans_rmse_m"]:.6f} | {rotation["rpe_rot_rmse_deg"]:.6f} |

## Interpretation

The 10 ms camera-IMU timestamp offset increased ATE RMSE from `{nominal["ate_rmse_m"]:.6f} m` to `{timestamp["ate_rmse_m"]:.6f} m`, a `{timestamp["ate_increase_x"]:.2f}x` increase on `MH_01_easy`.

In this measured run, 10 ms temporal offset was much less damaging than the 5 degree z-axis rotation perturbation, which increased ATE by `{rotation["ate_increase_x"]:.2f}x`.

This should not be generalized to all temporal offsets or motion profiles. It establishes an initial temporal-calibration sensitivity point and motivates a future timestamp sweep.

## Artifacts

- Table: `results/tables/mh01_timestamp_sensitivity_summary.csv`
- Plot: `results/plots/mh01_timestamp_sensitivity_ate_rmse.png`
- Source metrics: `results/metrics.csv`

## Caution

Only one timestamp perturbation magnitude is reported here: 10 ms on `MH_01_easy`. Larger offsets and additional sequences are needed before drawing broader conclusions.
"""
    report_path = Path("reports/mh01_timestamp_sensitivity.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)

    print(f"wrote {table}")
    print(f"wrote {plot}")
    print(f"wrote {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
