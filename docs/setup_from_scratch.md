# Setup From Scratch

This document explains how a fresh reviewer can inspect and reproduce this benchmark at two levels.

## Level 1: Reproduce checked-in artifacts

This mode does not require ROS 2, OpenVINS, or EuRoC bags. It uses checked-in metrics and trajectories to regenerate tables, plots, reports, the run manifest, and artifact checks.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pytest numpy matplotlib
./scripts/reproduce_checked_in_results.sh
./scripts/run_tests.sh
```

Expected result:

```text
OK: results/metrics.csv matches metrics schema
missing_paths: 0
OK: all referenced artifacts exist
pytest passes
```

## Level 2: Rerun OpenVINS experiments

This mode requires the local robotics stack used for the benchmark.

Expected local paths:

```text
EuRoC ROS 2 bags:   ~/datasets/euroc/ros2_bags/MH_01_easy
                     ~/datasets/euroc/ros2_bags/MH_03_medium
OpenVINS workspace: ~/openvins_ws_jazzy
```

The repository intentionally does not vendor EuRoC bags or OpenVINS build outputs.

## What this project is

A Camera-IMU calibration sensitivity benchmark for VIO failure analysis. It injects controlled extrinsic perturbations into OpenVINS camera-IMU configs, freezes online calibration, runs EuRoC sequences, evaluates with evo ATE/RPE, and documents failure behavior.

## What this project is not

This is not a camera-IMU calibration estimator and it does not claim to estimate intrinsics, extrinsics, or temporal offset from raw data. It measures downstream VIO sensitivity to known perturbations.

## Full rerun pattern

A full OpenVINS rerun uses two terminals.

Terminal 1:

```bash
bash scripts/run_openvins_prepared_run_generic.sh openvins_MH03_rot_z_5deg_full_000 perturbed
```

Terminal 2:

```bash
bash scripts/play_euroc_full_bag.sh MH_03_medium openvins_MH03_rot_z_5deg_full_000 perturbed
```

After playback ends, stop OpenVINS with Ctrl+C, convert the output to TUM format, evaluate with evo, and add the metrics row.

## Main engineering takeaways

1. Small calibration perturbations do not always degrade metrics monotonically.
2. In the measured runs, z-axis rotation perturbation is much more damaging than y-axis translation perturbation.
3. A VIO process can produce a full-length trajectory that is physically unusable.
4. ATE, RPE, trajectory completeness, and trajectory plots should be interpreted together.
5. Frozen online calibration isolates sensitivity but does not test estimator recovery.

## Core commands

```bash
./scripts/run_tests.sh
./scripts/reproduce_checked_in_results.sh
bash scripts/regenerate_reports.sh
python scripts/check_artifacts_exist.py
```
