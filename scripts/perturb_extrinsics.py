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


ROW_RE = re.compile(r"^(?P<indent>\s*)-\s*\[(?P<values>[^\]]+)\]\s*$")


def parse_row_values(line: str) -> list[float]:
    match = ROW_RE.match(line)
    if not match:
        raise ValueError(f"Not a matrix row: {line!r}")
    return [float(x.strip()) for x in match.group("values").split(",") if x.strip()]


def format_row(indent: str, values: list[float]) -> str:
    formatted = ", ".join(f"{v:.12g}" for v in values)
    return f"{indent}- [{formatted}]"


def perturb_imucam_yaml_text(text: str, axis: str, angle_deg: float) -> tuple[str, int]:
    lines = text.splitlines()
    output = []
    i = 0
    count = 0

    while i < len(lines):
        line = lines[i]
        output.append(line)

        if "T_imu_cam:" not in line:
            i += 1
            continue

        if i + 4 >= len(lines):
            raise ValueError("Found T_imu_cam but not enough following rows for a 4x4 matrix")

        matrix_lines = lines[i + 1 : i + 5]
        rows = []
        indents = []

        for row_line in matrix_lines:
            match = ROW_RE.match(row_line)
            if not match:
                raise ValueError(f"Expected matrix row after T_imu_cam, got: {row_line!r}")
            indents.append(match.group("indent"))
            rows.append(parse_row_values(row_line))

        if any(len(row) != 4 for row in rows):
            raise ValueError(f"Expected 4 values in each row, got row lengths: {[len(row) for row in rows]}")

        flat = [value for row in rows for value in row]
        T = make_transform(flat)
        T_new = perturb_T_imu_cam_rotation_left(T, axis=axis, angle_deg=angle_deg)
        new_rows = [flatten_transform(T_new)[j : j + 4] for j in range(0, 16, 4)]

        for indent, row_values in zip(indents, new_rows):
            output.append(format_row(indent, row_values))

        count += 1
        i += 5

    return "\n".join(output) + "\n", count


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply controlled rotation perturbation to all T_imu_cam matrices in a Kalibr imucam YAML."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--axis", required=True, choices=["x", "y", "z"])
    parser.add_argument("--angle-deg", required=True, type=float)
    args = parser.parse_args()

    text = args.input.read_text()
    new_text, count = perturb_imucam_yaml_text(text, args.axis, args.angle_deg)

    if count == 0:
        print("ERROR: no T_imu_cam matrices were perturbed")
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
