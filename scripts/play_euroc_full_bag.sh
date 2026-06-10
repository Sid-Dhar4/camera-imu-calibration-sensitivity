#!/usr/bin/env bash
set -eo pipefail

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  echo "Usage: bash scripts/play_euroc_full_bag.sh <sequence> <run_id> [nominal|perturbed]" >&2
  exit 2
fi

SEQUENCE="$1"
RUN_ID="$2"
RUN_GROUP="${3:-perturbed}"

if [ "$RUN_GROUP" != "nominal" ] && [ "$RUN_GROUP" != "perturbed" ]; then
  echo "ERROR: run group must be 'nominal' or 'perturbed'" >&2
  exit 2
fi

REPO="$HOME/robotics_ws/camera-imu-calibration-sensitivity"
BAG="$HOME/datasets/euroc/ros2_bags/${SEQUENCE}"
LOG_DIR="$REPO/results/logs/${RUN_GROUP}/${RUN_ID}"
LOG_PATH="$LOG_DIR/ros2_bag_play_full.log"

cd "$REPO"
deactivate 2>/dev/null || true
source /opt/ros/jazzy/setup.bash
source "$HOME/openvins_ws_jazzy/install/setup.bash"

if [ ! -d "$BAG" ]; then
  echo "Missing ROS2 bag directory: $BAG" >&2
  exit 1
fi

mkdir -p "$LOG_DIR"

printf "\n=== Terminal 3: play full EuRoC bag ===\n"
printf "Sequence: %s\n" "$SEQUENCE"
printf "Run ID: %s\n" "$RUN_ID"
printf "Run group: %s\n" "$RUN_GROUP"
printf "Bag: %s\n" "$BAG"
printf "Log: %s\n\n" "$LOG_PATH"
printf "Do not press Ctrl+C during playback.\n\n"

if ros2 bag play -h | grep -q -- "--disable-keyboard-controls"; then
  time ros2 bag play "$BAG" --disable-keyboard-controls 2>&1 | tee "$LOG_PATH"
else
  time ros2 bag play "$BAG" 2>&1 | tee "$LOG_PATH"
fi

printf "\nFull bag playback ended.\n"
printf "Now go to the OpenVINS terminal and press Ctrl+C once.\n"
