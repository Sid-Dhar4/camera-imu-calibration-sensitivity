#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path


def label_from_ms(value: float) -> str:
    if float(value).is_integer():
        text = str(int(value))
    else:
        text = str(value).replace(".", "p")
    text = text.replace("-", "neg")
    return f"timestamp_{text}ms"


def replace_time_offset(text: str, seconds: float) -> tuple[str, int]:
    lines = text.splitlines()
    out = []
    count = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("time_offset:"):
            indent = line[: len(line) - len(line.lstrip())]
            out.append(f"{indent}time_offset: {seconds:.9f}")
            count += 1
        else:
            out.append(line)
    if count == 0:
        raise ValueError("no time_offset field found")
    return "\n".join(out) + "\n", count


def freeze_estimator_config(text: str) -> str:
    replacements = {
        "calib_cam_extrinsics: true": "calib_cam_extrinsics: false",
        "calib_cam_intrinsics: true": "calib_cam_intrinsics: false",
        "calib_cam_timeoffset: true": "calib_cam_timeoffset: false",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def generate_one(sequence: str, magnitude_ms: float, source_dir: Path, output_root: Path) -> Path:
    magnitude_s = magnitude_ms / 1000.0
    out_dir = output_root / sequence / label_from_ms(magnitude_ms)
    out_dir.mkdir(parents=True, exist_ok=True)

    for name in ["kalibr_imucam_chain.yaml", "estimator_config.yaml"]:
        shutil.copy2(source_dir / name, out_dir / name)

    imu_text = (source_dir / "kalibr_imu_chain.yaml").read_text()
    imu_text, count = replace_time_offset(imu_text, magnitude_s)
    (out_dir / "kalibr_imu_chain.yaml").write_text(imu_text)

    est_text = (source_dir / "estimator_config.yaml").read_text()
    frozen = freeze_estimator_config(est_text)
    (out_dir / "estimator_config_frozen.yaml").write_text(frozen)

    (out_dir / "generation_log.txt").write_text("\n".join([
        f"sequence: {sequence}",
        "perturb_type: timestamp",
        f"magnitude_ms: {magnitude_ms}",
        f"magnitude_s: {magnitude_s:.9f}",
        f"time_offset_fields_perturbed: {count}",
        f"source_dir: {source_dir}",
        f"output_dir: {out_dir}",
    ]) + "\n")

    (out_dir / "freeze_log.txt").write_text("\n".join([
        f"input: {source_dir / 'estimator_config.yaml'}",
        f"output: {out_dir / 'estimator_config_frozen.yaml'}",
        "calib_cam_extrinsics: false",
        "calib_cam_intrinsics: false",
        "calib_cam_timeoffset: false",
    ]) + "\n")

    return out_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate timestamp-offset OpenVINS configs.")
    parser.add_argument("--sequence", required=True)
    parser.add_argument("--magnitudes-ms", nargs="+", type=float, required=True)
    parser.add_argument("--source-dir", default="configs/nominal/openvins/euroc_mav", type=Path)
    parser.add_argument("--output-root", default="configs/generated/openvins", type=Path)
    args = parser.parse_args()

    generated = []
    for mag in args.magnitudes_ms:
        generated.append(generate_one(args.sequence, mag, args.source_dir, args.output_root))

    print("generated_dirs:")
    for path in generated:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
