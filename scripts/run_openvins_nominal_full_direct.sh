#!/usr/bin/env bash
set -e

cd "$HOME/robotics_ws/camera-imu-calibration-sensitivity"

deactivate 2>/dev/null || true
source /opt/ros/jazzy/setup.bash
source "$HOME/openvins_ws_jazzy/install/setup.bash"

RUN_ID="openvins_MH01_nominal_full_000"
CONFIG_PATH="$HOME/robotics_ws/camera-imu-calibration-sensitivity/results/configs_used/${RUN_ID}/estimator_config_full_safe.yaml"
TRAJ_DIR="$HOME/robotics_ws/camera-imu-calibration-sensitivity/results/trajectories/nominal/${RUN_ID}"
LOG_PATH="$HOME/robotics_ws/camera-imu-calibration-sensitivity/results/logs/nominal/${RUN_ID}/openvins_full.log"

mkdir -p "$TRAJ_DIR" "$(dirname "$LOG_PATH")"
rm -f "$TRAJ_DIR/ov_estimate.txt" "$TRAJ_DIR/ov_estimate_std.txt" "$TRAJ_DIR/ov_groundtruth.txt" "$TRAJ_DIR/traj_timing.txt"

printf "\n=== Terminal 2: OpenVINS full nominal MH01 run ===\n"
printf "Run ID: %s\n" "$RUN_ID"
printf "Config: %s\n" "$CONFIG_PATH"
printf "Trajectory dir: %s\n" "$TRAJ_DIR"
printf "Log: %s\n\n" "$LOG_PATH"
printf "Leave this running until Terminal 3 says bag playback ended, then press Ctrl+C once here.\n\n"

stdbuf -oL -eL ros2 run ov_msckf run_subscribe_msckf \
  --ros-args \
  -r __ns:=/ov_msckf \
  -p config_path:="$CONFIG_PATH" \
  -p verbosity:=INFO \
  -p use_stereo:=true \
  -p max_cameras:=2 \
  -p save_total_state:=true \
  -p filepath_est:="$TRAJ_DIR/ov_estimate.txt" \
  -p filepath_std:="$TRAJ_DIR/ov_estimate_std.txt" \
  -p filepath_gt:="$TRAJ_DIR/ov_groundtruth.txt" \
  2>&1 | tee "$LOG_PATH"
