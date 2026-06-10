#!/usr/bin/env python3
import csv
from pathlib import Path

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
        ("0.0", "openvins_MH01_nominal_full_000"),
        ("0.5", "openvins_MH01_rot_z_0p5deg_full_000"),
        ("1.0", "openvins_MH01_rot_z_1deg_full_000"),
        ("2.0", "openvins_MH01_rot_z_2deg_full_000"),
        ("5.0", "openvins_MH01_rot_z_5deg_full_000"),
    ]
    summary = [(deg, find(rows, run_id)) for deg, run_id in specs]
    nominal = summary[0][1]
    rot5 = summary[-1][1]
    increase = float(rot5["ate_rmse_m"]) / float(nominal["ate_rmse_m"])

    table = Path("results/tables/mh01_rotation_z_sweep.csv")
    table.parent.mkdir(parents=True, exist_ok=True)
    with table.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rotation_z_deg", "ate_rmse_m", "rpe_trans_rmse_m", "rpe_rot_rmse_deg", "completion_rate", "status", "run_id"])
        for deg, row in summary:
            writer.writerow([deg, row["ate_rmse_m"], row["rpe_trans_rmse_m"], row["rpe_rot_rmse_deg"], row["completion_rate"], row["status"], row["run_id"]])

    report = Path("reports/mh01_rotation_z_sweep.md")
    report.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# MH_01_easy Rotation-Z Sweep", "", "## Summary", "", "| Rotation z perturbation (deg) | ATE RMSE (m) | RPE trans RMSE (m) | RPE rot RMSE (deg) |", "|---:|---:|---:|---:|"]
    for deg, row in summary:
        lines.append(f"| {deg} | {float(row['ate_rmse_m']):.6f} | {float(row['rpe_trans_rmse_m']):.6f} | {float(row['rpe_rot_rmse_deg']):.6f} |")
    lines.extend([
        "",
        "## Interpretation",
        "",
        f"The frozen-calibration nominal baseline has ATE RMSE `{float(nominal['ate_rmse_m']):.6f} m`.",
        "",
        f"The 5 degree rotation perturbation increases ATE RMSE from `{float(nominal['ate_rmse_m']):.6f} m` to `{float(rot5['ate_rmse_m']):.6f} m`, a `{increase:.2f}x` increase.",
        "",
        "Small perturbations should not be interpreted as improved calibration if they appear better than nominal; they may reflect estimator variance, alignment effects, or model mismatch.",
        "",
        "## Artifacts",
        "",
        "- Table: `results/tables/mh01_rotation_z_sweep.csv`",
        "- Source metrics: `results/metrics.csv`",
    ])
    report.write_text("\\n".join(lines) + "\\n")
    print(f"wrote {table}")
    print(f"wrote {report}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
