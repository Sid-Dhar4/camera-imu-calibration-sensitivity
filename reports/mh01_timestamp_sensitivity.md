# MH_01_easy Timestamp Sensitivity

## Purpose

This report adds a temporal calibration perturbation to the existing extrinsic calibration sensitivity benchmark.

## Summary

| Case | ATE RMSE (m) | Increase vs nominal | RPE trans RMSE (m) | RPE rot RMSE (deg) |
|---|---:|---:|---:|---:|
| nominal | 0.079973 | 1.00x | 0.032763 | 0.225416 |
| timestamp 10ms | 0.088672 | 1.11x | 0.030492 | 0.237766 |
| translation-y 5cm | 0.095484 | 1.19x | 0.003577 | 0.042328 |
| rotation-z 5deg | 2.064969 | 25.82x | 0.194584 | 0.343487 |

## Interpretation

The 10 ms camera-IMU timestamp offset increased ATE RMSE from `0.079973 m` to `0.088672 m`, a `1.11x` increase on `MH_01_easy`.

In this measured run, 10 ms temporal offset was much less damaging than the 5 degree z-axis rotation perturbation, which increased ATE by `25.82x`.

This should not be generalized to all temporal offsets or motion profiles. It establishes an initial temporal-calibration sensitivity point and motivates a future timestamp sweep.

## Artifacts

- Table: `results/tables/mh01_timestamp_sensitivity_summary.csv`
- Plot: `results/plots/mh01_timestamp_sensitivity_ate_rmse.png`
- Source metrics: `results/metrics.csv`

## Caution

Only one timestamp perturbation magnitude is reported here: 10 ms on `MH_01_easy`. Larger offsets and additional sequences are needed before drawing broader conclusions.
