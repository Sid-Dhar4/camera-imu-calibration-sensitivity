# Setup Discovery

Date: 2026-05-28

## Local system findings

- Host OS: Ubuntu 24.04-family system.
- ROS 2 Jazzy is available at /opt/ros/jazzy/bin/ros2.
- ROS 1 tools were not found in PATH during discovery.
- No existing OpenVINS workspace was found under the searched common folders.
- EuRoC ROS1 bag files were found under ~/datasets/euroc/bags/.
- evo and rosbags are installed in the project .venv.

## Dataset files found

- ~/datasets/euroc/bags/MH_01_easy.bag
- ~/datasets/euroc/bags/MH_03_medium.bag
- ~/datasets/euroc/bags/MH_05_difficult.bag

## Current runtime decision

Do not build OpenVINS blindly yet.

Next decision is whether to:
1. build OpenVINS natively against ROS 2 Jazzy,
2. use a Dockerized OpenVINS runtime,
3. or use another controlled OpenVINS path after confirming dependencies.

## Notes

The first estimator milestone remains a nominal OpenVINS run on MH_01_easy.
