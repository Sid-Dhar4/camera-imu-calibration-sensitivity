# MH_01_easy Rotation-vs-Translation Error Budget

## Purpose

This report compares the current camera-IMU rotation-z sensitivity sweep against the translation-y perturbation runs on EuRoC `MH_01_easy`.

## Key observation

On this sequence and estimator setup, the tested rotation perturbation produced a much larger degradation than the tested y-axis translation perturbations.

- Nominal ATE RMSE: `0.139204 m`
- Rotation-z 5 deg ATE RMSE: `2.064969 m`
- Translation-y 5 cm ATE RMSE: `0.095484 m`
- Translation-y 2 cm ATE RMSE: `0.073369 m`
- Translation-y 1 cm ATE RMSE: `0.100477 m`

The 5 degree z-axis rotation perturbation increased ATE RMSE by `14.83x` relative to nominal. The tested y-axis translation perturbations did not show the same collapse on this sequence.

## Artifacts

- Table: `results/tables/mh01_rotation_vs_translation_error_budget.csv`
- Plot: `results/plots/mh01_rotation_vs_translation_ate_rmse.png`
- Source metrics: `results/metrics.csv`

## Caution

This is not a universal calibration conclusion. It is a measured result for OpenVINS on EuRoC `MH_01_easy` using the current frozen-calibration setup. More axes and more sequences are needed before making broader claims.
