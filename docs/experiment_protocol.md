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

| Sequence | Nominal | Rotation-z sweep | Translation-y sweep |
|---|---:|---:|---:|
| MH_01_easy | yes | 0.5, 1, 2, 5 deg | 1, 2, 5 cm |
| MH_03_medium | yes | 5 deg | not yet reported |

## Perturbations

The current reported perturbations modify the camera-IMU extrinsic transform.

Reported perturbation families:

