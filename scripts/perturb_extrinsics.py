#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from calibration_perturb.transforms import (
    flatten_transform,
    make_transform,
    perturb_T_imu_cam_rotation_left,
)


DATA_RE = re.compile(r"data:\\s*\\[([^\\]]+)\\]")


def parse_numbers(data_text: str) -> list[float]:
    return [float(x.strip()) for x in data_text.replace("\\n", " ").split(",") if x.strip()]


def format_matrix_data(values: list[float]) -> str:
    if len(values) != 16:
        raise ValueError(f"Expected 16 values, got {len(values)}")
    formatted = ", ".join(f"{v:.12g}" for v in values)
    return f"data: [{formatted}]"


def perturb_imucam_yaml_text(text: str, axis: str, angle_deg: float) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match) -> str:
        nonlocal count
        nums = parse_numbers(match.group(1))
        if len(nums) != 16:
            return match.group(0)
        T = make_transform(nums)
        T_new = perturb_T_imu_cam_rotation_left(T, axis=axis, angle_deg=angle_deg)
        count += 1
        return format_matrix_data(flatten_transform(T_new))

    new_text = DATA_RE.sub(repl, text)
    return new_text, count


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply controlled rotation perturbation to all T_imu_cam matrices in a Kalibr imucam YAML.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--axis", required=True, choices=["x", "y", "z"])
    parser.add_argument("--angle-deg", required=True, type=float)
    args = parser.parse_args()

    text = args.input.read_text()
    new_text, count = perturb_imucam_yaml_text(text, args.axis, args.angle_deg)
    if count == 0:
        print("ERROR: no 4x4 data matrices were perturbed")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(new_text)

    print(f"input: {args.input}")
    print(f"output: {args.output}")
    print(f"axis: {args.axis}")
    print(f"angle_deg: {args.angle_deg}")
    print(f"matrices_perturbed: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
