# OpenVINS Build Notes

Date: 2026-05-28

## External workspace

```text
~/openvins_ws_jazzy
```

## Source state

Branch: pr-500-jazzy

Commit: 0bd027a 	modified:   ov_msckf/src/ros/ROS2Visualizer.cpp 	modified:   ov_msckf/src/ros/ROS2Visualizer.h 	modified:   ov_msckf/src/run_simulation.cpp 	modified:   ov_msckf/src/run_subscribe_msckf.cpp

## Build issue encountered

Initial OpenVINS build failed in `ov_init` because CMake could not find Ceres:

```text
CeresConfig.cmake
ceres-config.cmake
```

## Fix

Installed and verified `libceres-dev`, then rebuilt OpenVINS from a clean build/install/log state.

## Build command

```bash
cd ~/openvins_ws_jazzy
source /opt/ros/jazzy/setup.bash
colcon build --event-handlers console_direct+ --parallel-workers 2 --cmake-args -DCMAKE_BUILD_TYPE=Release
```

## Logs

```text
results/logs/setup/openvins_colcon_build.txt
results/logs/setup/openvins_colcon_build_after_ceres_fix.txt
results/logs/setup/openvins_rosdep_check_before_install.txt
results/logs/setup/openvins_rosdep_install.txt
results/logs/setup/openvins_rosdep_check_after_install.txt
results/logs/setup/openvins_rosdep_check_after_direct_ceres_install.txt
results/logs/setup/ceres_config_paths_after_install.txt
results/logs/setup/openvins_ros2_pkg_list.txt
results/logs/setup/openvins_ov_msckf_executables.txt
results/logs/setup/openvins_ov_msckf_prefix.txt
results/logs/setup/openvins_installed_launch_files.txt
results/logs/setup/openvins_euroc_config_files.txt
```

No VIO result is claimed yet. This only documents the runtime build.
