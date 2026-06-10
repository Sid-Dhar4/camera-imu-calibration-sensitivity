# Multi-sequence Rotation-z 5 Degree Sensitivity

## Purpose

This report compares the effect of a 5 degree camera-IMU z-axis rotation perturbation on two EuRoC MAV sequences.

## Summary

| Sequence | Nominal ATE RMSE (m) | Rotation-z 5deg ATE RMSE (m) | Increase |
|---|---:|---:|---:|
| MH_01_easy | 0.139204 | 2.064969 | 14.83x |
| MH_03_medium | 0.107259 | 831.507723 | 7752.34x |

## Key observation

The 5 degree z-axis camera-IMU rotation perturbation degrades both sequences, but the effect is much larger on `MH_03_medium`.

On `MH_01_easy`, ATE RMSE increases from `0.139204 m` to `2.064969 m`.

On `MH_03_medium`, ATE RMSE increases from `0.107259 m` to `831.507723 m`, indicating severe trajectory divergence despite the estimator producing an output trajectory.

## Artifacts

- Table: `results/tables/mh01_mh03_rotation_z_5deg_summary.csv`
- Plot: `results/plots/mh01_mh03_rotation_z_5deg_ate_rmse.png`
- Source metrics: `results/metrics.csv`

## Caution

This is a measured result for OpenVINS on two EuRoC machine-hall sequences with frozen camera calibration. It should not yet be generalized to all datasets, all motion profiles, or all VIO systems.
