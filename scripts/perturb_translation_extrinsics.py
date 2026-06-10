#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from calibration_perturb.transforms import flatten_transform
from calibration_perturb.transforms import make_transform
from calibration_perturb.transforms import perturb_T_imu_cam_translation_imu_frame


ROW_RE = re.compile(r"^(?P<indent>\s*)-\s*\[(?P<values>[^\]]+)\]\s*$")


def parse_row_values(line: str) -> list[float]:
    match = ROW_RE.match(line)
    if not match:
        raise ValueError(f"Could not parse matrix row: {line}")
    return [float(x.strip()) for x in match.group("values").split(",")]


def format_row(indent: str, values: list[float]) -> str:
    formatted = ", ".join(f"{v:.12g}" for v in values)
    return f"{indent}- [{formatted}]"


def perturb_imucam_yaml_translation_text(text: str, axis: str, magnitude_m: float) -> tuple[str, int]:
    lines = text.splitlines()
    output = []
    i = 0
    count = 0

    while i < len(lines):
        output.append(lines[i])
        if "T_imu_cam:" not in lines[i]:
            i += 1
            continue

        if i + 4 >= len(lines):
            raise ValueError("T_imu_cam block ended unexpectedly")

        row_lines = lines[i + 1 : i + 5]
        rows = []
        indents = []
        for row_line in row_lines:
            match = ROW_RE.match(row_line)
            if not match:
                raise ValueError(f"Invalid T_imu_cam row: {row_line}")
            indents.append(match.group("indent"))
            rows.append(parse_row_values(row_line))

        flat = [value for row in rows for value in row]
        T = make_transform(flat)
        T_new = perturb_T_imu_cam_translation_imu_frame(T, axis=axis, magnitude_m=magnitude_m)
        new_rows = [flatten_transform(T_new)[j : j + 4] for j in range(0, 16, 4)]

        for indent, row in zip(indents, new_rows):
            output.append(format_row(indent, row))

        count += 1
        i += 5

    return "\n".join(output) + "\n", count


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply translation perturbation to all T_imu_cam matrices in a Kalibr imucam YAML.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--axis", required=True, choices=["x", "y", "z"])
    parser.add_argument("--magnitude-m", required=True, type=float)
    args = parser.parse_args()

    text = args.input.read_text()
    new_text, count = perturb_imucam_yaml_translation_text(text, args.axis, args.magnitude_m)
    if count == 0:
        print("ERROR: no T_imu_cam matrices were perturbed")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(new_text)
    print(f"input: {args.input}")
    print(f"output: {args.output}")
    print(f"axis: {args.axis}")
    print(f"magnitude_m: {args.magnitude_m}")
    print(f"matrices_perturbed: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
