# Project Tracker

## Current milestone
- Milestone number: 5
- Goal: Run one nominal OpenVINS MH_01_easy test and locate trajectory output.
- Status: prepared_pending_launch_review
- Blockers: Need to inspect launch/config logs from Batch 5A-5B and choose exact Terminal 2/Terminal 3 commands.
- Next command to run: review OpenVINS launch args and run nominal smoke test.

## Completed milestones
| Milestone | Date | Artifact | Commit |
|---|---|---|---|
| 1 | 2026-05-28 | Repo skeleton, metrics schema, initial tests, tracker | 4f998e9, a431b17 |
| 2 | 2026-05-28 | Local Python/evo/rosbags tooling and dataset discovery | 29ae6f5, bafe8b9 |
| 3 | 2026-05-28 | MH_01_easy ROS 2 bag conversion script and verification log | 843ed21 |
| 4 | 2026-05-28 | OpenVINS ROS 2 build and Ceres fix | 9f69189, f4f0a4f |
| 5-prep | 2026-05-28 | Nominal MH_01 config snapshot and launch inspection logs | pending |

## Run tracker
| run_id | sequence | perturbation | status | output path | notes |
|---|---|---|---|---|
| openvins_MH01_nominal_000 | MH_01_easy | nominal | prepared_not_run | results/trajectories/nominal/openvins_MH01_nominal_000 | config copied, not launched yet |

## Metrics tracker
| sequence | perturbation | ATE RMSE | RPE trans | RPE rot | status |
|---|---:|---:|---:|---:|---|

## Open questions
- What exact launch arguments does subscribe.launch.py require?
- Does OpenVINS save trajectory output by default?
- Which topic or file should be used as first trajectory output?
- Does bag playback need --clock or use_sim_time?

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

## Failure log
| Date | Failure | Cause | Fix | Lesson |
|---|---|---|---|---|
| 2026-05-28 | Python __pycache__ files were committed in the initial commit | .gitignore did not exist before pytest ran | Added .gitignore and removed caches from Git tracking | Run repo hygiene checks before commits |
| 2026-05-28 | venv pytest loaded ROS launch_testing plugin and failed on missing lark | External pytest plugin autoload from ROS environment | Added scripts/run_tests.sh with PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 | Isolate project tests from ROS environment plugins |
| 2026-05-28 | OpenVINS build failed in ov_init | CMake could not find CeresConfig.cmake / ceres-config.cmake | Installed/verified libceres-dev and rebuilt from clean build state | Save build logs and inspect exact package failure before changing code |
