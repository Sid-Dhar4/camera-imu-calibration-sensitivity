#!/usr/bin/env bash
set -euo pipefail

cd "$HOME/robotics_ws/camera-imu-calibration-sensitivity"
source .venv/bin/activate

RUN_ID="openvins_MH01_nominal_full_000"
GT_TUM="results/trajectories/groundtruth/MH_01_easy_gt.tum"
EST_TUM="results/trajectories/nominal/${RUN_ID}/openvins_estimate.tum"
EVO_DIR="results/evo/${RUN_ID}"
PLOT_DIR="results/plots"

mkdir -p "$EVO_DIR" "$PLOT_DIR"

printf "\nCleaning old evo outputs for this run...\n"
rm -f "$EVO_DIR/ape_console.txt" "$EVO_DIR/rpe_trans_console.txt" "$EVO_DIR/rpe_rot_console.txt"
rm -f "$EVO_DIR/ape_results.zip" "$EVO_DIR/rpe_trans_results.zip" "$EVO_DIR/rpe_rot_results.zip"
rm -f "$EVO_DIR/evo_summary.json" "$EVO_DIR/evo_summary_console.txt"

printf "\n=== evo APE: MH01 nominal OpenVINS ===\n"
printf "GT:  %s\n" "$GT_TUM"
printf "EST: %s\n" "$EST_TUM"

evo_ape tum "$GT_TUM" "$EST_TUM" \
  -a \
  --t_max_diff 0.01 \
  --save_results "$EVO_DIR/ape_results.zip" \
  2>&1 | tee "$EVO_DIR/ape_console.txt"

printf "\n=== evo RPE translation: MH01 nominal OpenVINS ===\n"
printf "Using delta=20 frames, approximately 1 second for 20 Hz OpenVINS output.\n"
evo_rpe tum "$GT_TUM" "$EST_TUM" \
  -a \
  --t_max_diff 0.01 \
  --pose_relation trans_part \
  --delta 20 \
  --delta_unit f \
  --save_results "$EVO_DIR/rpe_trans_results.zip" \
  2>&1 | tee "$EVO_DIR/rpe_trans_console.txt"

printf "\n=== evo RPE rotation: MH01 nominal OpenVINS ===\n"
printf "Using delta=20 frames, approximately 1 second for 20 Hz OpenVINS output.\n"
evo_rpe tum "$GT_TUM" "$EST_TUM" \
  -a \
  --t_max_diff 0.01 \
  --pose_relation angle_deg \
  --delta 20 \
  --delta_unit f \
  --save_results "$EVO_DIR/rpe_rot_results.zip" \
  2>&1 | tee "$EVO_DIR/rpe_rot_console.txt"

printf "\nEvo outputs:\n"
find "$EVO_DIR" -maxdepth 1 -type f -printf "%p %k KB\n" | sort
