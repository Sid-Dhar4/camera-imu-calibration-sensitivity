#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt


def collect_error_budget_rows(metrics_path: Path, sequence: str) -> list[dict]:
    rows = list(csv.DictReader(metrics_path.open()))

    wanted = []
    for row in rows:
        if row["sequence"] != sequence:
            continue

        if row["perturb_type"] == "nominal":
            label = "nominal"
            magnitude = 0.0
            units = "none"
        elif row["perturb_type"] == "rotation" and row["perturb_axis"] == "z":
            label = f"rotation_z_{row['perturb_magnitude']}deg"
            magnitude = float(row["perturb_magnitude"])
            units = "deg"
        elif row["perturb_type"] == "translation" and row["perturb_axis"] == "y":
            label = f"translation_y_{row['perturb_magnitude']}cm"
            magnitude = float(row["perturb_magnitude"])
            units = "cm"
        else:
            continue

        wanted.append({
            "label": label,
            "perturb_type": row["perturb_type"],
            "axis": row["perturb_axis"],
            "magnitude": magnitude,
            "units": units,
            "ate_rmse_m": float(row["ate_rmse_m"]),
            "rpe_trans_rmse_m": float(row["rpe_trans_rmse_m"]),
            "rpe_rot_rmse_deg": float(row["rpe_rot_rmse_deg"]),
            "completion_rate": float(row["completion_rate"]) if row["completion_rate"] else "",
        })

    type_order = {"nominal": 0, "rotation": 1, "translation": 2}
    wanted.sort(key=lambda r: (type_order.get(r["perturb_type"], 99), r["magnitude"]))
    return wanted


def write_table(rows: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "label",
        "perturb_type",
        "axis",
        "magnitude",
        "units",
        "ate_rmse_m",
        "rpe_trans_rmse_m",
        "rpe_rot_rmse_deg",
        "completion_rate",
    ]
    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_plot(rows: list[dict], output_path: Path, sequence: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    labels = [r["label"] for r in rows]
    ates = [r["ate_rmse_m"] for r in rows]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, ates)
    plt.ylabel("ATE RMSE (m)")
    plt.title(f"{sequence} calibration sensitivity: rotation-z vs translation-y")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()


def find_row(rows: list[dict], label: str) -> dict:
    for row in rows:
        if row["label"] == label:
            return row
    raise ValueError(f"missing required row: {label}")


def write_report(rows: list[dict], output_path: Path, table_path: Path, plot_path: Path, sequence: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    nominal = find_row(rows, "nominal")
    rot5 = find_row(rows, "rotation_z_5.0deg")
    trans5 = find_row(rows, "translation_y_5.0cm")
    trans2 = find_row(rows, "translation_y_2.0cm")
    trans1 = find_row(rows, "translation_y_1.0cm")

    report = f"""# {sequence} Rotation-vs-Translation Error Budget

## Purpose

This report compares the current camera-IMU rotation-z sensitivity sweep against the translation-y perturbation runs on EuRoC `{sequence}`.

## Key observation

On this sequence and estimator setup, the tested rotation perturbation produced a much larger degradation than the tested y-axis translation perturbations.

- Nominal ATE RMSE: `{nominal['ate_rmse_m']:.6f} m`
- Rotation-z 5 deg ATE RMSE: `{rot5['ate_rmse_m']:.6f} m`
- Translation-y 5 cm ATE RMSE: `{trans5['ate_rmse_m']:.6f} m`
- Translation-y 2 cm ATE RMSE: `{trans2['ate_rmse_m']:.6f} m`
- Translation-y 1 cm ATE RMSE: `{trans1['ate_rmse_m']:.6f} m`

The 5 degree z-axis rotation perturbation increased ATE RMSE by `{rot5['ate_rmse_m'] / nominal['ate_rmse_m']:.2f}x` relative to nominal. The tested y-axis translation perturbations did not show the same collapse on this sequence.

## Artifacts

- Table: `{table_path}`
- Plot: `{plot_path}`
- Source metrics: `results/metrics.csv`

## Caution

This is not a universal calibration conclusion. It is a measured result for OpenVINS on EuRoC `{sequence}` using the current frozen-calibration setup. More axes and more sequences are needed before making broader claims.
"""
    output_path.write_text(report)


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize rotation-vs-translation calibration error budget.")
    parser.add_argument("--metrics", default="results/metrics.csv", type=Path)
    parser.add_argument("--sequence", default="MH_01_easy")
    parser.add_argument("--table", default="results/tables/mh01_rotation_vs_translation_error_budget.csv", type=Path)
    parser.add_argument("--plot", default="results/plots/mh01_rotation_vs_translation_ate_rmse.png", type=Path)
    parser.add_argument("--report", default="reports/mh01_rotation_vs_translation_error_budget.md", type=Path)
    args = parser.parse_args()

    rows = collect_error_budget_rows(args.metrics, args.sequence)
    write_table(rows, args.table)
    write_plot(rows, args.plot, args.sequence)
    write_report(rows, args.report, args.table, args.plot, args.sequence)

    print(f"wrote {args.table}")
    print(f"wrote {args.plot}")
    print(f"wrote {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
