# Project Tracker

## Current milestone
- Milestone number: 2
- Goal: Locate or reproduce a known working OpenVINS EuRoC nominal run.
- Status: in_progress
- Blockers: OpenVINS runtime not installed yet.
- Next command to run: choose OpenVINS runtime path after reviewing Batch 2B-2E output.

## Completed milestones
| Milestone | Date | Artifact | Commit |
|---|---|---|---|
| 1 | 2026-05-28 | Repo skeleton, metrics schema, initial tests, tracker | 4f998e9, a431b17 |

## Run tracker
| run_id | sequence | perturbation | status | output path | notes |
|---|---|---|---|---|

## Metrics tracker
| sequence | perturbation | ATE RMSE | RPE trans | RPE rot | status |
|---|---:|---:|---:|---:|---|

## Open questions
- Should OpenVINS be built natively on ROS 2 Jazzy or isolated in Docker?
- Do the existing EuRoC bags need conversion to ROS 2 bag format?
- What exact OpenVINS command will produce the trajectory file for evo?

## Decisions made
- Project is a separate repo.
- MVP uses OpenVINS only.
- MVP uses EuRoC MH_01_easy first, then MH_03_medium.
- Timestamp perturbation is deferred.
- Online calibration and recovery are deferred.
- Failed runs will be logged as data.
- Python cache files are ignored and removed from Git tracking.
- Host Python tools live in .venv.

## Failure log
| Date | Failure | Cause | Fix | Lesson |
|---|---|---|---|---|
| 2026-05-28 | Python __pycache__ files were committed in the initial commit | .gitignore did not exist before pytest ran | Added .gitignore and removed caches from Git tracking | Run repo hygiene checks before commits |
