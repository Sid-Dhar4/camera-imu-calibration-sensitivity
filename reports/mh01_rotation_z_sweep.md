# MH_01_easy Rotation-z Calibration Sensitivity Sweep

## Summary

This sweep evaluates OpenVINS on EuRoC MH_01_easy under controlled camera-IMU z-axis rotation perturbations.

Camera extrinsic, camera intrinsic, and camera-IMU time offset optimization were disabled during these runs. This keeps the injected perturbation fixed rather than allowing the estimator to optimize it away.

## Results

| Rotation z perturbation (deg) | ATE RMSE (m) | RPE trans RMSE (m) | RPE rot RMSE (deg) |
|---:|---:|---:|---:|
| 0.0 | 0.139204 | 0.048954 | 0.268658 |
| 0.5 | 0.100281 | 0.029226 | 0.229276 |
| 1.0 | 0.117957 | 0.033253 | 0.260834 |
| 2.0 | 0.188732 | 0.042565 | 0.237368 |
| 5.0 | 2.064969 | 0.194584 | 0.343487 |

## Main observation

The 5 degree rotation perturbation increases ATE RMSE from 0.139204 m to 2.064969 m, a 14.83x increase.

Smaller perturbations from 0.5 to 2 degrees remain much closer to the nominal result on this sequence. This suggests that, for this axis and sequence, the estimator is tolerant to small z-axis camera-IMU rotation errors but degrades sharply at larger error.

## Important limitations

- This is one sequence: EuRoC MH_01_easy.
- This sweep tests z-axis rotation only.
- Results should not be generalized to all axes, all trajectories, or all VIO systems.
- These runs use SE(3) alignment without scale correction.
- Small perturbations appearing better than nominal should not be interpreted as calibration improvement; they may reflect estimator variance, alignment effects, or model mismatch.
