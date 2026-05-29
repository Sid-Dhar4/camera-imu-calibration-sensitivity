# Project Tracker

## Current milestone
- Milestone number: 1
- Goal: Create repo skeleton, tracker, sweep config placeholders, and metrics schema.
- Status: in_progress
- Blockers: none
- Next command to run: python3 scripts/check_results_schema.py results/metrics.csv

## Completed milestones
| Milestone | Date | Artifact | Commit |
|---|---|---|---|

## Run tracker
| run_id | sequence | perturbation | status | output path | notes |
|---|---|---|---|---|

## Metrics tracker
| sequence | perturbation | ATE RMSE | RPE trans | RPE rot | status |
|---|---:|---:|---:|---:|---|

## Open questions
- Which existing OpenVINS environment from the VIO benchmark project can be reused?
- Where will EuRoC data be stored locally?
- Which OpenVINS trajectory output format will be easiest to evaluate with evo?

## Decisions made
- Project is a separate repo.
- MVP uses OpenVINS only.
- MVP uses EuRoC MH_01_easy first, then MH_03_medium.
- Timestamp perturbation is deferred.
- Online calibration and recovery are deferred.
- Failed runs will be logged as data.

## Failure log
| Date | Failure | Cause | Fix | Lesson |
|---|---|---|---|---|
