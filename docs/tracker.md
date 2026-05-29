# Project Tracker

## Current milestone
- Milestone number: 4
- Goal: Create or acquire a working OpenVINS ROS 2 runtime for nominal MH_01_easy.
- Status: not_started
- Blockers: OpenVINS source/runtime not built yet.
- Next command to run: inspect OpenVINS Jazzy branch/build path.

## Completed milestones
| Milestone | Date | Artifact | Commit |
|---|---|---|---|
| 1 | 2026-05-28 | Repo skeleton, metrics schema, initial tests, tracker | 4f998e9, a431b17 |
| 2 | 2026-05-28 | Local Python/evo/rosbags tooling and dataset discovery | 29ae6f5, bafe8b9 |
| 3 | 2026-05-28 | MH_01_easy ROS 2 bag conversion script and verification log | pending |

## Run tracker
| run_id | sequence | perturbation | status | output path | notes |
|---|---|---|---|---|

## Metrics tracker
| sequence | perturbation | ATE RMSE | RPE trans | RPE rot | status |
|---|---:|---:|---:|---:|---|

## Open questions
- Should OpenVINS be built from the ROS 2 Jazzy PR branch or another stable branch?
- What exact OpenVINS command will produce a trajectory file for evo?
- Are extra dependencies needed for OpenVINS on Ubuntu 24.04/Jazzy?

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

## Failure log
| Date | Failure | Cause | Fix | Lesson |
|---|---|---|---|---|
| 2026-05-28 | Python __pycache__ files were committed in the initial commit | .gitignore did not exist before pytest ran | Added .gitignore and removed caches from Git tracking | Run repo hygiene checks before commits |
| 2026-05-28 | venv pytest loaded ROS launch_testing plugin and failed on missing lark | External pytest plugin autoload from ROS environment | Added scripts/run_tests.sh with PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 | Isolate project tests from ROS environment plugins |
