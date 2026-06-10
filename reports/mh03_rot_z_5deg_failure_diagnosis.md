# MH_03_medium Rotation-Z 5 Degree Failure Diagnosis

## Purpose

This report explains the severe `MH_03_medium` failure observed under a 5 degree z-axis camera-IMU rotation perturbation.

## Key observation

| Run | ATE RMSE (m) | RPE trans RMSE (m) | RPE rot RMSE (deg) | Trajectory rows | Duration (s) | Completion |
|---|---:|---:|---:|---:|---:|---:|
| nominal | 0.107259 | 0.004381 | 0.018141 | 2311 | 115.500 | 0.849802 |
| rotation-z 5deg | 831.507723 | 1.944413 | 0.072117 | 2311 | 115.500 | 0.849802 |

The 5 degree z-axis perturbation increases ATE RMSE by `7752.34x` relative to nominal while still producing a trajectory with the same estimated duration and completion rate.

## Why this is a VIO failure, not just a missing-output case

- OpenVINS produced an output trajectory instead of crashing.
- The estimated trajectory has `2311` TUM poses over `115.500` seconds.
- The completion rate is `0.849802`, matching the nominal run for this sequence.
- The failure appears as severe global trajectory inconsistency, not as a simple absence of estimates.

## Why ATE can be catastrophic while RPE rotation is not

ATE measures global position consistency after time association and SE(3) alignment. RPE rotation measures local relative orientation error over a fixed frame interval. A trajectory can have locally smooth relative orientation while its global position estimate drifts or diverges badly. Therefore, the combination of huge ATE, high RPE translation, and modest RPE rotation is plausible and should be interpreted as global translational trajectory failure rather than pure orientation jitter.

## Trajectory geometry summary

| Run | Estimated path length (m) | Start-to-end displacement (m) | Max radius from start (m) |
|---|---:|---:|---:|
| nominal | 128.756096 | 0.127576 | 9.996465 |
| rotation-z 5deg | 3154.533011 | 2974.618027 | 2974.618027 |

## Related artifacts

- Table: `results/tables/mh03_rot_z_5deg_failure_diagnosis.csv`
- Aligned XY plot: `results/plots/mh03_gt_nominal_rot5_aligned_xy.png`
- Aligned XZ plot: `results/plots/mh03_gt_nominal_rot5_aligned_xz.png`
- Source metrics: `results/metrics.csv`

## Caution

This diagnosis does not claim that every 5 degree camera-IMU rotation error always causes this magnitude of failure. It documents one controlled OpenVINS run on EuRoC `MH_03_medium` with frozen calibration and checked-in evo evaluation artifacts.
