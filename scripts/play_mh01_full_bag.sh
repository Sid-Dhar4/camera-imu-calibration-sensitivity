#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: bash scripts/play_mh01_full_bag.sh <run_id>" >&2
  exit 2
fi

RUN_ID="$1"
REPO="$HOME/robotics_ws/camera-imu-calibration-sensitivity"
BAG="$HOME/datasets/euroc/ros2_bags/MH_01_easy"
LOG_DIR="$REPO/results/logs/perturbed/${RUN_ID}"
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

printf "\n=== Terminal 3: play full MH_01_easy bag ===\n"
printf "Run ID: %s\n" "$RUN_ID"
printf "Bag: %s\n" "$BAG"
printf "Log: %s\n\n" "$LOG_PATH"
printf "This should take about 188 seconds plus overhead. Do not press Ctrl+C.\n\n"

if ros2 bag play -h | grep -q -- "--disable-keyboard-controls"; then
  time ros2 bag play "$BAG" --disable-keyboard-controls 2>&1 | tee "$LOG_PATH"
else
  time ros2 bag play "$BAG" 2>&1 | tee "$LOG_PATH"
fi

printf "\nFull bag playback ended.\n"
printf "Now go to Terminal 2 and press Ctrl+C once.\n"
