#!/usr/bin/env bash
set -e

cd "$HOME/robotics_ws/camera-imu-calibration-sensitivity"

deactivate 2>/dev/null || true
source /opt/ros/jazzy/setup.bash
source "$HOME/openvins_ws_jazzy/install/setup.bash"

RUN_ID="openvins_MH01_nominal_000"
BAG="$HOME/datasets/euroc/ros2_bags/MH_01_easy"
LOG_PATH="$HOME/robotics_ws/camera-imu-calibration-sensitivity/results/logs/nominal/${RUN_ID}/ros2_bag_play_direct_smoke.log"

mkdir -p "$(dirname "$LOG_PATH")"

printf "\n=== Terminal 3: play MH_01_easy smoke bag ===\n"
printf "Bag: %s\n" "$BAG"
printf "Log: %s\n\n" "$LOG_PATH"
printf "Playing for about 60 seconds. Do not press Ctrl+C. timeout should stop it.\n\n"

if ros2 bag play -h | grep -q -- "--disable-keyboard-controls"; then
  timeout 60s ros2 bag play "$BAG" --disable-keyboard-controls 2>&1 | tee "$LOG_PATH"
else
  timeout 60s ros2 bag play "$BAG" 2>&1 | tee "$LOG_PATH"
fi

printf "\nBag playback ended.\n"
printf "Now go to Terminal 2 and press Ctrl+C once.\n"
