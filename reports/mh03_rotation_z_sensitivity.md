# MH_03_medium Rotation-z Sensitivity

## Purpose

This report summarizes OpenVINS sensitivity to z-axis camera-IMU rotation perturbations on EuRoC `MH_03_medium`.

## Summary

| Run | ATE RMSE (m) | Increase vs nominal | RPE trans RMSE (m) | RPE rot RMSE (deg) |
|---|---:|---:|---:|---:|
| nominal | 0.107259 | 1.00x | 0.004381 | 0.018141 |
| rotation-z 2deg | 0.353662 | 3.30x | 0.094482 | 0.268001 |
| rotation-z 5deg | 831.507723 | 7752.34x | 1.944413 | 0.072117 |

## Interpretation

The 2 degree rotation-z perturbation increases ATE RMSE from `0.107259 m` to `0.353662 m`, a `3.30x` increase.

The 5 degree rotation-z perturbation increases ATE RMSE to `831.507723 m`, a `7752.34x` increase. This indicates severe trajectory divergence even though OpenVINS produced an output trajectory.

This result suggests a threshold-like behavior on `MH_03_medium`: moderate degradation at 2 degrees, followed by catastrophic degradation at 5 degrees.

## Artifacts

- Table: `results/tables/mh03_rotation_z_sensitivity.csv`
- Plot: `results/plots/mh03_rotation_z_sensitivity_ate_rmse.png`
- Source metrics: `results/metrics.csv`

## Caution

This is a measured result for OpenVINS on one EuRoC sequence with frozen camera calibration. It should not be generalized to all motion profiles, all datasets, or all VIO systems.
