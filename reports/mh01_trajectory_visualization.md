# MH_01_easy Trajectory Visualization

## Purpose

This visualization compares the EuRoC MH_01_easy ground-truth trajectory against OpenVINS trajectories from the nominal run and the z-axis 5 degree camera-IMU rotation perturbation run.

The trajectories are time-associated and SE(3)-aligned to ground truth before plotting, matching the alignment assumption used in evo evaluation.

## Files

- `results/plots/mh01_gt_nominal_rot5_aligned_xy.png`
- `results/plots/mh01_gt_nominal_rot5_aligned_xz.png`

## Interpretation

The nominal trajectory is expected to remain close to ground truth after alignment. The 5 degree perturbation trajectory is expected to show larger deviation, consistent with the ATE RMSE increase reported in the rotation-z sweep.

## Limitation

These plots are qualitative visualizations. The quantitative results are reported in `results/metrics.csv` and `reports/mh01_rotation_z_sweep.md`.
