# Reproducibility Notes

This document explains what is required to reproduce the current benchmark results.

## Scope

This repository contains the benchmark code, generated OpenVINS configs, trajectory outputs, metrics, plots, and reports for the completed runs.

It does not vendor EuRoC MAV bags or the OpenVINS source tree. Those are external dependencies.

## Required local inputs

The current scripts assume these local paths:

```text
~/datasets/euroc/ros2_bags/MH_01_easy
~/datasets/euroc/ros2_bags/MH_03_medium
~/openvins_ws_jazzy
```

The EuRoC bags are expected to be available in ROS 2 bag format before running OpenVINS.

## Python checks

From the repository root:

```bash
source .venv/bin/activate
./scripts/run_tests.sh
python scripts/check_results_schema.py results/metrics.csv
```

The test suite checks metrics schema validation, calibration perturbation math, config generation, run-specific config preparation, and trajectory alignment helpers.

## What can be rerun from checked-in files

The following can be rerun directly from this repository:

- Python tests
- metrics schema validation
- summary table generation
- summary report generation
- trajectory overlay plotting from checked-in TUM trajectories

The full OpenVINS runs require the external EuRoC ROS 2 bags and OpenVINS workspace.

## Current expected test status

At the time of the current public result, the local Python test suite passes with:

```text
21 passed
```
