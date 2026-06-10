# Project Reassessment

## Current score

Technical reality: 8/10  
Reproducibility: 7.5/10  
Portfolio presentation: 4.5/10  
Interview defensibility: 7/10  
Big-company signal: 6.8/10  

Overall current state: about 7/10.

## Why this is real now

The repo has a nominal OpenVINS EuRoC run, frozen-calibration perturbation setup, a generated camera-IMU rotation perturbation, and evo evaluation showing measurable degradation.

Measured first result:

- Nominal ATE RMSE: 0.139204 m
- Rotation z +5 deg ATE RMSE: 2.064969 m
- ATE degradation: 14.834x

## Why this is not 9.5+ yet

The project currently has one perturbation point. A strong validation study needs sweeps, plots, tables, and a report.

## Minimum strong portfolio version

1. Full MH_01_easy rotation z sweep: 0, 0.5, 1, 2, 5 degrees.
2. Full MH_01_easy translation sweep: 0, 0.5, 1, 2, 5 cm.
3. Automated run/eval/metrics scripts.
4. Sensitivity plots.
5. Error-budget report.
6. README reproduction commands.
7. Honest failure cases and limitations.

## 9.5+ version

1. Add MH_03_medium.
2. Add x/y/z axis coverage or justify the chosen axes.
3. Add status/failure threshold table.
4. Add demo video script and interview notes.
5. Keep recovery/Kalibr as future work unless actually measured.
