# Project Tracker

## Current milestone
- Milestone number: 11
- Goal: Implement first controlled camera-IMU rotation perturbation generator.
- Status: not_started
- Blockers: none for nominal baseline; perturbation generator not implemented yet.
- Next command to run: create transform utilities and rotation perturbation test.

## Completed milestones
| Milestone | Date | Artifact | Commit |
|---|---|---|---|
| 1 | 2026-05-28 | Repo skeleton, metrics schema, initial tests, tracker | 4f998e9, a431b17 |
| 2 | 2026-05-28 | Local Python/evo/rosbags tooling and dataset discovery | 29ae6f5, bafe8b9 |
| 3 | 2026-05-28 | MH_01_easy ROS 2 bag conversion script and verification log | 843ed21 |
| 4 | 2026-05-28 | OpenVINS ROS 2 build and Ceres fix | 9f69189, f4f0a4f |
| 5 | 2026-05-29 | Nominal MH01 smoke run succeeded | f695496 |
| 6 | 2026-05-29 | Full nominal MH01 OpenVINS run | a491830 |
| 7 | 2026-05-29 | OpenVINS trajectory converted to TUM | 943188a |
| 8 | 2026-05-29 | EuRoC ground truth converted to TUM | 65535bb |
| 9 | 2026-05-29 | evo ATE/RPE evaluation complete | 8d0901a, be2f019 |
| 10 | 2026-05-29 | First evaluated nominal metrics.csv row | pending |

## Run tracker
| run_id | sequence | perturbation | status | output path | notes |
|---|---|---|---|---|
| openvins_MH01_nominal_full_000 | MH_01_easy | nominal | success | results/trajectories/nominal/openvins_MH01_nominal_full_000/openvins_estimate.tum | ATE/RPE evaluated with evo |

## Metrics tracker
| sequence | perturbation | ATE RMSE | RPE trans | RPE rot | status |
|---|---:|---:|---:|---:|---|
| MH_01_easy | nominal | 0.139204 m | 0.048954 m | 0.268658 deg | success |

## Open questions
- Which perturbation convention should be used first: left-multiply R_CtoI about IMU z-axis.
- Should calibration online optimization be frozen before perturbation sweeps? Yes, for sensitivity measurement.

## Decisions made
- Project is a separate repo.
- MVP uses OpenVINS only.
- MVP uses EuRoC MH_01_easy first, then MH_03_medium.
- Timestamp perturbation is deferred.
- Online calibration and recovery are deferred.
- Failed runs will be logged as data.
- Python cache files are ignored and removed from Git tracking.
- Host Python tools live in .venv.
- MH_01_easy is converted first; MH_03_medium waits until nominal MH_01 works.
- OpenVINS source lives outside the benchmark repo under ~/openvins_ws_jazzy/src/open_vins.
- OpenVINS build required direct verification of Ceres/libceres-dev.
- Nominal OpenVINS configs are copied into the benchmark repo before any perturbation.
- Evo evaluation uses SE(3) alignment without scale correction.
- RPE uses delta 20 frames, approximately 1 second for 20 Hz OpenVINS output.

## Failure log
| Date | Failure | Cause | Fix | Lesson |
|---|---|---|---|---|
| 2026-05-28 | Python __pycache__ files were committed in the initial commit | .gitignore did not exist before pytest ran | Added .gitignore and removed caches from Git tracking | Run repo hygiene checks before commits |
| 2026-05-28 | venv pytest loaded ROS launch_testing plugin and failed on missing lark | External pytest plugin autoload from ROS environment | Added scripts/run_tests.sh with PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 | Isolate project tests from ROS environment plugins |
| 2026-05-28 | OpenVINS build failed in ov_init | CMake could not find CeresConfig.cmake / ceres-config.cmake | Installed/verified libceres-dev and rebuilt from clean build state | Save build logs and inspect exact package failure before changing code |
| 2026-05-28 | OpenVINS smoke run crashed at startup | save_total_state used default output filenames with empty parent paths | Passed explicit filepath_est/filepath_std/filepath_gt parameters | Treat startup crashes as environment/config issues, not estimator failures |
| 2026-05-29 | evo_rpe failed with delta_unit=s | This evo version accepts f/d/r/m, not seconds | Used delta 20 frames with delta_unit f | Verify CLI options against installed tool version |
