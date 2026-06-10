#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "== Validate metrics schema =="
python scripts/check_results_schema.py results/metrics.csv

echo "== Generate run manifest =="
python scripts/generate_run_manifest.py

echo "== Regenerate MH01 rotation-vs-translation error budget =="
python scripts/summarize_error_budget.py
python scripts/summarize_mh01_rotation_z_sweep.py

echo "== Regenerate MH01/MH03 rotation-z 5deg multi-sequence summary =="
python scripts/summarize_multisequence_rot5.py

echo "== Regenerate MH03 rotation-z sensitivity summary =="
python scripts/summarize_mh03_rotation_z_sensitivity.py

echo "== Regenerate MH03 rotation-vs-translation error budget =="
python scripts/summarize_mh03_rotation_vs_translation.py

echo "== Regenerate MH03 rotation-z 5deg failure diagnosis =="
python scripts/diagnose_mh03_rot_z_5deg_failure.py

echo "== Regenerate MH01 aligned trajectory plots =="
python scripts/plot_aligned_tum_trajectories.py \
  --groundtruth results/trajectories/groundtruth/MH_01_easy_gt.tum \
  --estimate nominal results/trajectories/nominal/openvins_MH01_nominal_full_000/openvins_estimate.tum \
  --estimate rotation_z_5deg results/trajectories/perturbed/openvins_MH01_rot_z_5deg_full_000/openvins_estimate.tum \
  --output-prefix results/plots/mh01_gt_nominal_rot5_aligned \
  --max-dt 0.01

echo "== Regenerate MH03 aligned trajectory plots =="
python scripts/plot_aligned_tum_trajectories.py \
  --groundtruth results/trajectories/groundtruth/MH_03_medium_gt.tum \
  --estimate nominal results/trajectories/nominal/openvins_MH03_nominal_full_000/openvins_estimate.tum \
  --estimate rotation_z_5deg results/trajectories/perturbed/openvins_MH03_rot_z_5deg_full_000/openvins_estimate.tum \
  --output-prefix results/plots/mh03_gt_nominal_rot5_aligned \
  --max-dt 0.01

echo "== Check referenced artifacts =="
python scripts/check_reported_configs_frozen.py
python scripts/check_artifacts_exist.py

echo "== Done =="
