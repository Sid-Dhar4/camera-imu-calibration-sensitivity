#!/usr/bin/env bash
set -e

if [ "$#" -ne 2 ]; then
  printf "Usage: scripts/convert_euroc_ros1_to_ros2.sh /path/to/input.bag /path/to/output_bag_dir\n"
  exit 2
fi

SRC_BAG="$1"
DST_DIR="$2"

if [ ! -f "$SRC_BAG" ]; then
  printf "ERROR: source bag does not exist: %s\n" "$SRC_BAG"
  exit 1
fi

if [ -e "$DST_DIR" ]; then
  printf "ERROR: destination already exists: %s\n" "$DST_DIR"
  printf "Move or delete it intentionally before rerunning.\n"
  exit 1
fi

printf "Source bag: %s\n" "$SRC_BAG"
printf "Destination: %s\n" "$DST_DIR"
printf "Storage: sqlite3\n"
printf "Source typestore: ros1_noetic\n"
printf "Destination typestore: ros2_jazzy\n"

mkdir -p "$(dirname "$DST_DIR")"

rosbags-convert \
  --src "$SRC_BAG" \
  --dst "$DST_DIR" \
  --dst-storage sqlite3 \
  --src-typestore ros1_noetic \
  --dst-typestore ros2_jazzy

printf "Conversion complete: %s\n" "$DST_DIR"
