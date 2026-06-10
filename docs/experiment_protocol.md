# Experiment Protocol

This document defines the current benchmark protocol.

## Goal

Measure how controlled camera-IMU calibration perturbations affect visual-inertial odometry accuracy.

The benchmark is not intended to prove universal calibration limits. It is a controlled study of OpenVINS behavior on selected EuRoC MAV sequences under frozen calibration settings.

## Estimator

The current estimator is OpenVINS.

Online calibration of camera extrinsics, camera intrinsics, and camera-IMU time offset is disabled for the reported runs. This is intentional: the goal is to measure the effect of injected calibration error, not to let the estimator recover it online.

## Datasets

Current reported sequences:

```text
EuRoC MAV MH_01_easy
EuRoC MAV MH_03_medium
```

Current completed coverage:

| Sequence | Nominal | Rotation-z sweep | Translation-y sweep | Timestamp offset |
|---|---:|---:|---:|---:|
| MH_01_easy | yes | 0.5, 1, 2, 5 deg | 1, 2, 5 cm | 10 ms |
| MH_03_medium | yes | 2, 5 deg | 5 cm | not yet reported |

## Perturbations

The current reported perturbations modify the camera-IMU extrinsic transform.

Reported perturbation families:

```text
rotation about IMU z axis
translation along IMU y axis
camera-IMU timestamp offset
```

Each run uses a generated config copied into `results/configs_used/<run_id>/`.

## Metrics

| Metric | Meaning |
|---|---|
| ATE RMSE | absolute trajectory error after SE(3) alignment |
| RPE translation RMSE | relative translational drift over a fixed frame delta |
| RPE rotation RMSE | relative rotational drift over a fixed frame delta |
| completion rate | estimated trajectory duration divided by bag duration |

ATE and RPE are computed with evo. ATE uses SE(3) alignment with no scale correction.

## Interpretation rules

A lower ATE/RPE value for a perturbed run should not be interpreted as improved calibration without additional repeated trials and broader validation.

A run can have `status=success` if OpenVINS produced an output trajectory, even if the resulting trajectory is physically unusable.

Large ATE, large RPE, or visual divergence should be interpreted as accuracy failure even when the process itself completed.

## Current main finding

On MH_01_easy, a 5 degree z-axis rotation perturbation increased ATE RMSE from 0.079973 m to 2.064969 m.

On MH_03_medium, a 2 degree z-axis rotation perturbation increased ATE RMSE from 0.107259 m to 0.353662 m. A 5 degree perturbation increased ATE RMSE to 831.507723 m.

For the current MH_01_easy translation-y sweep, perturbations from 1 to 5 cm stayed near nominal ATE. On MH_03_medium, the reported 5 cm translation-y perturbation also stayed near nominal ATE. On MH_01_easy, a 10 ms timestamp offset increased ATE RMSE from 0.079973 m to 0.088672 m.

## Limitations

- only one estimator is reported
- only two EuRoC sequences are reported
- only z-axis rotation and y-axis translation are reported
- MH_03_medium has nominal, rotation-z 2/5 degree, and translation-y 5 cm results, but does not yet have a full perturbation sweep
- only one timestamp perturbation is reported so far: 10 ms on MH_01_easy
- recovery experiments are planned but not reported
