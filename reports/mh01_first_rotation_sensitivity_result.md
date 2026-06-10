# MH_01 First Rotation Sensitivity Result

## Result summary

This first measured perturbation compares the nominal OpenVINS MH_01_easy run against a frozen-calibration run with a +5 degree z-axis camera-IMU rotation perturbation.

| Metric | Nominal | Rotation z +5 deg | Ratio |
|---|---:|---:|---:|
| ATE RMSE (m) | 0.139204 | 2.064969 | 14.834x |
| RPE trans RMSE (m) | 0.048954 | 0.194584 | 3.975x |
| RPE rot RMSE (deg) | 0.268658 | 0.343487 | 1.279x |

## Interpretation

A 5 degree camera-IMU rotation perturbation increased ATE RMSE from 0.139204 m to 2.064969 m on MH_01_easy.

This is the first evidence that the benchmark is measuring calibration sensitivity rather than merely rerunning VIO.

## Important limitations

- This is one perturbation point, not a full sweep.
- The result is on MH_01_easy only.
- The next step is to run a rotation sweep across smaller magnitudes: 0.5, 1, 2, and 5 degrees.
- Translation perturbation has not been evaluated yet.
- No recovery or Kalibr comparison is claimed.
