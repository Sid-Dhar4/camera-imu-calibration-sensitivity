#!/usr/bin/env python3
import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from freeze_openvins_calibration import freeze_calibration_text
from perturb_extrinsics import perturb_imucam_yaml_text


def magnitude_label(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return str(value).replace(".", "p")


def generate_one(
    nominal_dir: Path,
    output_root: Path,
    sequence: str,
    axis: str,
    magnitude_deg: float,
) -> Path:
    label = magnitude_label(magnitude_deg)
    out_dir = output_root / sequence / f"rotation_{axis}_{label}deg"
    out_dir.mkdir(parents=True, exist_ok=True)

    nominal_estimator = nominal_dir / "estimator_config.yaml"
    nominal_imu = nominal_dir / "kalibr_imu_chain.yaml"
    nominal_imucam = nominal_dir / "kalibr_imucam_chain.yaml"

    if not nominal_estimator.exists():
        raise FileNotFoundError(nominal_estimator)
    if not nominal_imu.exists():
        raise FileNotFoundError(nominal_imu)
    if not nominal_imucam.exists():
        raise FileNotFoundError(nominal_imucam)

    shutil.copy2(nominal_estimator, out_dir / "estimator_config.yaml")
    shutil.copy2(nominal_imu, out_dir / "kalibr_imu_chain.yaml")

    perturbed_text, count = perturb_imucam_yaml_text(
        nominal_imucam.read_text(),
        axis=axis,
        angle_deg=magnitude_deg,
    )
    if count == 0:
        raise RuntimeError("no T_imu_cam matrices were perturbed")

    (out_dir / "kalibr_imucam_chain.yaml").write_text(perturbed_text)

    frozen_text, counts = freeze_calibration_text(nominal_estimator.read_text())
    bad_counts = {k: v for k, v in counts.items() if v != 1}
    if bad_counts:
        raise RuntimeError(f"unexpected calibration flag counts: {counts}")

    (out_dir / "estimator_config_frozen.yaml").write_text(frozen_text)

    (out_dir / "generation_log.txt").write_text(
        "\n".join(
            [
                f"sequence: {sequence}",
                f"axis: {axis}",
                f"angle_deg: {magnitude_deg}",
                f"matrices_perturbed: {count}",
                f"source_imucam: {nominal_imucam}",
                f"output_imucam: {out_dir / 'kalibr_imucam_chain.yaml'}",
            ]
        )
        + "\n"
    )

    (out_dir / "freeze_log.txt").write_text(
        "\n".join(
            [
                f"input: {nominal_estimator}",
                f"output: {out_dir / 'estimator_config_frozen.yaml'}",
                "calib_cam_extrinsics: false",
                "calib_cam_intrinsics: false",
                "calib_cam_timeoffset: false",
            ]
        )
        + "\n"
    )

    return out_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate OpenVINS camera-IMU rotation perturbation configs.")
    parser.add_argument("--sequence", default="MH_01_easy")
    parser.add_argument("--axis", required=True, choices=["x", "y", "z"])
    parser.add_argument("--magnitudes-deg", required=True, nargs="+", type=float)
    parser.add_argument("--nominal-dir", default="configs/nominal/openvins/euroc_mav", type=Path)
    parser.add_argument("--output-root", default="configs/generated/openvins", type=Path)
    args = parser.parse_args()

    generated = []
    for magnitude in args.magnitudes_deg:
        out_dir = generate_one(
            nominal_dir=args.nominal_dir,
            output_root=args.output_root,
            sequence=args.sequence,
            axis=args.axis,
            magnitude_deg=magnitude,
        )
        generated.append(out_dir)

    print("generated_dirs:")
    for out_dir in generated:
        print(out_dir)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
