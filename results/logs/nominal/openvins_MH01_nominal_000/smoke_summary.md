# Nominal Smoke Run Summary

Run ID: openvins_MH01_nominal_000
Sequence: MH_01_easy
Backend: OpenVINS
Status: smoke_success

## Result

OpenVINS started, subscribed to EuRoC stereo/IMU topics, initialized, and wrote state/timing outputs.

## Evidence

- openvins_direct_smoke_success.txt contains successful initialization logs.
- ros2_bag_play_direct_smoke_success.txt contains ROS 2 bag playback logs.
- smoke_output_line_counts.txt records non-header output files.
- ov_estimate.txt contains estimated state rows.

## Important limitation

This is only a smoke run, not a full evaluated trajectory benchmark yet.
