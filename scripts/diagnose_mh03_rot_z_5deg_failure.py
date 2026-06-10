#!/usr/bin/env python3
import argparse
import csv
import math
from pathlib import Path


def read_metrics(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def find_metric(rows: list[dict], run_id: str) -> dict:
    for row in rows:
        if row["run_id"] == run_id:
            return row
    raise ValueError(f"missing metrics row for {run_id}")


def read_tum(path: Path) -> list[tuple[float, float, float, float]]:
    poses = []
    for line in path.read_text().splitlines():
        parts = line.strip().split()
        if len(parts) >= 4:
            poses.append((float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])))
    return poses


def path_length(poses: list[tuple[float, float, float, float]]) -> float:
    total = 0.0
    for a, b in zip(poses, poses[1:]):
        dx = b[1] - a[1]
        dy = b[2] - a[2]
        dz = b[3] - a[3]
        total += math.sqrt(dx * dx + dy * dy + dz * dz)
    return total


def displacement(poses: list[tuple[float, float, float, float]]) -> float:
    first = poses[0]
    last = poses[-1]
    dx = last[1] - first[1]
    dy = last[2] - first[2]
    dz = last[3] - first[3]
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def max_radius_from_start(poses: list[tuple[float, float, float, float]]) -> float:
    first = poses[0]
    best = 0.0
    for p in poses:
        dx = p[1] - first[1]
        dy = p[2] - first[2]
        dz = p[3] - first[3]
        best = max(best, math.sqrt(dx * dx + dy * dy + dz * dz))
    return best


def summarize_run(run_id: str, group: str, metric: dict) -> dict:
    tum = Path("results/trajectories") / group / run_id / "openvins_estimate.tum"
    poses = read_tum(tum)
    return {
        "run_id": run_id,
        "sequence": metric["sequence"],
        "perturb_type": metric["perturb_type"],
        "axis": metric["perturb_axis"],
        "magnitude": metric["perturb_magnitude"],
        "units": metric["perturb_units"],
        "trajectory_rows": len(poses),
        "first_timestamp": poses[0][0],
        "last_timestamp": poses[-1][0],
        "duration_s": poses[-1][0] - poses[0][0],
        "ate_rmse_m": float(metric["ate_rmse_m"]),
        "rpe_trans_rmse_m": float(metric["rpe_trans_rmse_m"]),
        "rpe_rot_rmse_deg": float(metric["rpe_rot_rmse_deg"]),
        "completion_rate": float(metric["completion_rate"]),
        "estimate_path_length_m": path_length(poses),
        "estimate_start_to_end_displacement_m": displacement(poses),
        "estimate_max_radius_from_start_m": max_radius_from_start(poses),
    }


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict], path: Path) -> None:
    nominal, rot5 = rows
    ate_ratio = rot5["ate_rmse_m"] / nominal["ate_rmse_m"]
    report = f"""# MH_03_medium Rotation-Z 5 Degree Failure Diagnosis

## Purpose

This report explains the severe `MH_03_medium` failure observed under a 5 degree z-axis camera-IMU rotation perturbation.

## Key observation

| Run | ATE RMSE (m) | RPE trans RMSE (m) | RPE rot RMSE (deg) | Trajectory rows | Duration (s) | Completion |
|---|---:|---:|---:|---:|---:|---:|
| nominal | {nominal["ate_rmse_m"]:.6f} | {nominal["rpe_trans_rmse_m"]:.6f} | {nominal["rpe_rot_rmse_deg"]:.6f} | {nominal["trajectory_rows"]} | {nominal["duration_s"]:.3f} | {nominal["completion_rate"]:.6f} |
| rotation-z 5deg | {rot5["ate_rmse_m"]:.6f} | {rot5["rpe_trans_rmse_m"]:.6f} | {rot5["rpe_rot_rmse_deg"]:.6f} | {rot5["trajectory_rows"]} | {rot5["duration_s"]:.3f} | {rot5["completion_rate"]:.6f} |

The 5 degree z-axis perturbation increases ATE RMSE by `{ate_ratio:.2f}x` relative to nominal while still producing a trajectory with the same estimated duration and completion rate.

## Why this is a VIO failure, not just a missing-output case

- OpenVINS produced an output trajectory instead of crashing.
- The estimated trajectory has `{rot5["trajectory_rows"]}` TUM poses over `{rot5["duration_s"]:.3f}` seconds.
- The completion rate is `{rot5["completion_rate"]:.6f}`, matching the nominal run for this sequence.
- The failure appears as severe global trajectory inconsistency, not as a simple absence of estimates.

## Why ATE can be catastrophic while RPE rotation is not

ATE measures global position consistency after time association and SE(3) alignment. RPE rotation measures local relative orientation error over a fixed frame interval. A trajectory can have locally smooth relative orientation while its global position estimate drifts or diverges badly. Therefore, the combination of huge ATE, high RPE translation, and modest RPE rotation is plausible and should be interpreted as global translational trajectory failure rather than pure orientation jitter.

## Trajectory geometry summary

| Run | Estimated path length (m) | Start-to-end displacement (m) | Max radius from start (m) |
|---|---:|---:|---:|
| nominal | {nominal["estimate_path_length_m"]:.6f} | {nominal["estimate_start_to_end_displacement_m"]:.6f} | {nominal["estimate_max_radius_from_start_m"]:.6f} |
| rotation-z 5deg | {rot5["estimate_path_length_m"]:.6f} | {rot5["estimate_start_to_end_displacement_m"]:.6f} | {rot5["estimate_max_radius_from_start_m"]:.6f} |

## Related artifacts

- Table: `results/tables/mh03_rot_z_5deg_failure_diagnosis.csv`
- Aligned XY plot: `results/plots/mh03_gt_nominal_rot5_aligned_xy.png`
- Aligned XZ plot: `results/plots/mh03_gt_nominal_rot5_aligned_xz.png`
- Source metrics: `results/metrics.csv`

## Caution

This diagnosis does not claim that every 5 degree camera-IMU rotation error always causes this magnitude of failure. It documents one controlled OpenVINS run on EuRoC `MH_03_medium` with frozen calibration and checked-in evo evaluation artifacts.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report)


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnose MH03 rotation-z 5 degree VIO failure.")
    parser.add_argument("--metrics", default="results/metrics.csv")
    parser.add_argument("--table", default="results/tables/mh03_rot_z_5deg_failure_diagnosis.csv")
    parser.add_argument("--report", default="reports/mh03_rot_z_5deg_failure_diagnosis.md")
    args = parser.parse_args()

    metrics = read_metrics(Path(args.metrics))
    nominal = summarize_run("openvins_MH03_nominal_full_000", "nominal", find_metric(metrics, "openvins_MH03_nominal_full_000"))
    rot5 = summarize_run("openvins_MH03_rot_z_5deg_full_000", "perturbed", find_metric(metrics, "openvins_MH03_rot_z_5deg_full_000"))
    rows = [nominal, rot5]
    write_csv(rows, Path(args.table))
    write_report(rows, Path(args.report))
    print(f"wrote {args.table}")
    print(f"wrote {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
