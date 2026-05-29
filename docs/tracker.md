# Project Tracker

## Current milestone
- Milestone number: 2
- Goal: Locate or reproduce a known working OpenVINS EuRoC nominal run.
- Status: not_started
- Blockers: OpenVINS runtime and EuRoC data location not confirmed yet.
- Next command to run: Batch 2A environment discovery.

## Completed milestones
| Milestone | Date | Artifact | Commit |
|---|---|---|---|
| 1 | 2026-05-28 | Repo skeleton, metrics schema, initial tests, tracker | 4f998e9 plus cleanup commit |

## Run tracker
| run_id | sequence | perturbation | status | output path | notes |
|---|---|---|---|---|

## Metrics tracker
| sequence | perturbation | ATE RMSE | RPE trans | RPE rot | status |
|---|---:|---:|---:|---:|---|

## Open questions
- Which existing OpenVINS environment from the VIO benchmark project can be reused?
- Where is EuRoC data stored locally?
- Are MH_01_easy and MH_03_medium already downloaded?
- Which OpenVINS command successfully produces a trajectory file on this machine?

## Decisions made
- Project is a separate repo.
- MVP uses OpenVINS only.
- MVP uses EuRoC MH_01_easy first, then MH_03_medium.
- Timestamp perturbation is deferred.
- Online calibration and recovery are deferred.
- Failed runs will be logged as data.
- Python cache files are ignored and removed from Git tracking.

## Failure log
| Date | Failure | Cause | Fix | Lesson |
|---|---|---|---|---|
| 2026-05-28 | Python __pycache__ files were committed in the initial commit | .gitignore did not exist before pytest ran | Added .gitignore and removed caches from Git tracking | Run repo hygiene checks before commits |
