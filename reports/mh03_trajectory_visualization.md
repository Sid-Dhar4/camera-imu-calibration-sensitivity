# MH_03_medium Trajectory Visualization

## Purpose

This visualization compares the EuRoC MH_03_medium ground-truth trajectory against the OpenVINS nominal run and the z-axis 5 degree camera-IMU rotation perturbation run.

The trajectories are time-associated and SE(3)-aligned to ground truth before plotting, matching the alignment assumption used in evo evaluation.

## Files

- `results/plots/mh03_gt_nominal_rot5_aligned_xy.png`
- `results/plots/mh03_gt_nominal_rot5_aligned_xz.png`

## Interpretation

The nominal trajectory remains close to ground truth after alignment. The 5 degree rotation perturbation shows severe trajectory divergence, consistent with the MH_03_medium ATE RMSE increase from `0.107259 m` to `831.507723 m`.

## Limitation

These plots are qualitative visualizations. The quantitative results are reported in `results/metrics.csv` and `reports/mh01_mh03_rotation_z_5deg_summary.md`.
