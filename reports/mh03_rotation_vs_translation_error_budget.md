# MH_03_medium Rotation-vs-Translation Error Budget

## Purpose

This report compares z-axis camera-IMU rotation perturbations against y-axis camera-IMU translation perturbation on EuRoC `MH_03_medium`.

## Summary

| Case | ATE RMSE (m) | Increase vs nominal | RPE trans RMSE (m) | RPE rot RMSE (deg) |
|---|---:|---:|---:|---:|
| nominal | 0.107259 | 1.00x | 0.004381 | 0.018141 |
| rotation-z 2deg | 0.353662 | 3.30x | 0.094482 | 0.268001 |
| rotation-z 5deg | 831.507723 | 7752.34x | 1.944413 | 0.072117 |
| translation-y 5cm | 0.111380 | 1.04x | 0.046137 | 0.174455 |

## Interpretation

On `MH_03_medium`, the 5 cm y-axis translation perturbation stays close to nominal ATE RMSE: `0.107259 m` nominal versus `0.111380 m` perturbed.

The z-axis rotation perturbations are more damaging: 2 degrees increases ATE by `3.30x`, while 5 degrees causes severe trajectory divergence with a `7752.34x` ATE increase.

This supports the current error-budget pattern: for the tested axes and magnitudes, z-axis camera-IMU rotation error is much more harmful than y-axis camera-IMU translation error.

## Artifacts

- Table: `results/tables/mh03_rotation_vs_translation_error_budget.csv`
- Plot: `results/plots/mh03_rotation_vs_translation_ate_rmse.png`
- Source metrics: `results/metrics.csv`

## Caution

This is a measured result for OpenVINS on one EuRoC sequence with frozen camera calibration. It should not be generalized to all axes, all datasets, or all VIO systems.
