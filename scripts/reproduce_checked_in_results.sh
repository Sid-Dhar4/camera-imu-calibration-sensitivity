#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== Reproduce checked-in benchmark artifacts =="
echo "This mode does not run OpenVINS and does not require ROS 2 bags."
echo "It regenerates tables, plots, reports, run manifest, and artifact checks from checked-in metrics and trajectories."

python scripts/check_results_schema.py results/metrics.csv
python scripts/generate_run_manifest.py
python scripts/summarize_error_budget.py
python scripts/summarize_multisequence_rot5.py
python scripts/summarize_mh03_rotation_z_sensitivity.py
python scripts/summarize_mh03_rotation_vs_translation.py
python scripts/diagnose_mh03_rot_z_5deg_failure.py

python scripts/plot_aligned_tum_trajectories.py \
  --groundtruth results/trajectories/groundtruth/MH_01_easy_gt.tum \
  --estimate nominal results/trajectories/nominal/openvins_MH01_nominal_full_000/openvins_estimate.tum \
  --estimate rotation_z_5deg results/trajectories/perturbed/openvins_MH01_rot_z_5deg_full_000/openvins_estimate.tum \
  --output-prefix results/plots/mh01_gt_nominal_rot5_aligned \
  --max-dt 0.01

python scripts/plot_aligned_tum_trajectories.py \
  --groundtruth results/trajectories/groundtruth/MH_03_medium_gt.tum \
  --estimate nominal results/trajectories/nominal/openvins_MH03_nominal_full_000/openvins_estimate.tum \
  --estimate rotation_z_5deg results/trajectories/perturbed/openvins_MH03_rot_z_5deg_full_000/openvins_estimate.tum \
  --output-prefix results/plots/mh03_gt_nominal_rot5_aligned \
  --max-dt 0.01

python scripts/check_artifacts_exist.py

echo "== Done: checked-in artifacts reproduced =="
