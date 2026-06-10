#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path


def replace_required(text: str, old: str, new: str) -> str:
    if old not in text:
        raise ValueError(f"required pattern not found: {old}")
    return text.replace(old, new)


def prepare_run_config(
    run_id: str,
    source_config_dir: Path,
    output_root: Path,
    log_root: Path,
    trajectory_root: Path,
    evo_root: Path,
    perturb_type: str,
    perturb_axis: str,
    perturb_magnitude: str,
    perturb_units: str,
    sequence: str,
) -> Path:
    run_group = "nominal" if perturb_type == "nominal" else "perturbed"

    run_config_dir = output_root / run_id
    run_log_dir = log_root / run_group / run_id
    run_traj_dir = trajectory_root / run_group / run_id
    run_evo_dir = evo_root / run_group / run_id

    if run_config_dir.exists():
        shutil.rmtree(run_config_dir)

    run_config_dir.mkdir(parents=True, exist_ok=True)
    run_log_dir.mkdir(parents=True, exist_ok=True)
    run_traj_dir.mkdir(parents=True, exist_ok=True)
    run_evo_dir.mkdir(parents=True, exist_ok=True)

    sources = {
        "estimator_config_frozen.yaml": "estimator_config.yaml",
        "kalibr_imucam_chain.yaml": "kalibr_imucam_chain.yaml",
        "kalibr_imu_chain.yaml": "kalibr_imu_chain.yaml",
    }

    for src_name, dst_name in sources.items():
        src = source_config_dir / src_name
        if not src.exists():
            raise FileNotFoundError(src)
        shutil.copy2(src, run_config_dir / dst_name)

    cfg = run_config_dir / "estimator_config.yaml"
    text = cfg.read_text()

    text = replace_required(text, "save_total_state: false", "save_total_state: true")
    text = replace_required(
        text,
        'filepath_est: "/tmp/ov_estimate.txt"',
        f'filepath_est: "{run_traj_dir / "ov_estimate.txt"}"',
    )
    text = replace_required(
        text,
        'filepath_std: "/tmp/ov_estimate_std.txt"',
        f'filepath_std: "{run_traj_dir / "ov_estimate_std.txt"}"',
    )
    text = replace_required(
        text,
        'filepath_gt: "/tmp/ov_groundtruth.txt"',
        f'filepath_gt: "{run_traj_dir / "ov_groundtruth.txt"}"',
    )
    text = replace_required(text, "record_timing_information: false", "record_timing_information: true")
    text = replace_required(
        text,
        'record_timing_filepath: "/tmp/traj_timing.txt"',
        f'record_timing_filepath: "{run_traj_dir / "traj_timing.txt"}"',
    )

    cfg.write_text(text)

    metadata = run_log_dir / "run_metadata.yaml"
    metadata.write_text(
        "\n".join(
            [
                f"run_id: {run_id}",
                f"sequence: {sequence}",
                "backend: openvins",
                f"perturb_type: {perturb_type}",
                f"perturb_axis: {perturb_axis}",
                f"perturb_magnitude: {perturb_magnitude}",
                f"perturb_units: {perturb_units}",
                "status: prepared_not_run",
                f"config_path: {run_config_dir / 'estimator_config.yaml'}",
                f"trajectory_output: {run_traj_dir / 'ov_estimate.txt'}",
                f"notes: camera calibration flags frozen; full {sequence} run configuration",
            ]
        )
        + "\n"
    )

    return run_config_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a run-specific OpenVINS config snapshot.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--source-config-dir", required=True, type=Path)
    parser.add_argument("--sequence", default="MH_01_easy")
    parser.add_argument("--perturb-type", required=True)
    parser.add_argument("--perturb-axis", required=True)
    parser.add_argument("--perturb-magnitude", required=True)
    parser.add_argument("--perturb-units", required=True)
    parser.add_argument("--output-root", default=Path("results/configs_used"), type=Path)
    parser.add_argument("--log-root", default=Path("results/logs"), type=Path)
    parser.add_argument("--trajectory-root", default=Path("results/trajectories"), type=Path)
    parser.add_argument("--evo-root", default=Path("results/evo"), type=Path)
    args = parser.parse_args()

    out = prepare_run_config(
        run_id=args.run_id,
        source_config_dir=args.source_config_dir,
        output_root=args.output_root,
        log_root=args.log_root,
        trajectory_root=args.trajectory_root,
        evo_root=args.evo_root,
        perturb_type=args.perturb_type,
        perturb_axis=args.perturb_axis,
        perturb_magnitude=args.perturb_magnitude,
        perturb_units=args.perturb_units,
        sequence=args.sequence,
    )

    print(f"prepared_run_config: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
