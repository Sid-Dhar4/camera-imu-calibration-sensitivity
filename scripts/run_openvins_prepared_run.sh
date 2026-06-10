#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: bash scripts/run_openvins_prepared_run.sh <run_id>" >&2
  exit 2
fi

RUN_ID="$1"
REPO="$HOME/robotics_ws/camera-imu-calibration-sensitivity"
CONFIG_PATH="$REPO/results/configs_used/${RUN_ID}/estimator_config.yaml"
TRAJ_DIR="$REPO/results/trajectories/perturbed/${RUN_ID}"
LOG_DIR="$REPO/results/logs/perturbed/${RUN_ID}"
LOG_PATH="$LOG_DIR/openvins_full.log"

cd "$REPO"
deactivate 2>/dev/null || true
source /opt/ros/jazzy/setup.bash
source "$HOME/openvins_ws_jazzy/install/setup.bash"

if [ ! -f "$CONFIG_PATH" ]; then
  echo "Missing config: $CONFIG_PATH" >&2
  exit 1
fi

mkdir -p "$TRAJ_DIR" "$LOG_DIR"
rm -f "$TRAJ_DIR/ov_estimate.txt" "$TRAJ_DIR/ov_estimate_std.txt" "$TRAJ_DIR/ov_groundtruth.txt" "$TRAJ_DIR/traj_timing.txt"

printf "\n=== Terminal 2: OpenVINS prepared run ===\n"
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
