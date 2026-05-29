#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


CALIB_FLAGS_TO_FREEZE = [
    "calib_cam_extrinsics",
    "calib_cam_intrinsics",
    "calib_cam_timeoffset",
]


def freeze_calibration_text(text: str) -> tuple[str, dict]:
    counts = {key: 0 for key in CALIB_FLAGS_TO_FREEZE}
    lines = []

    for line in text.splitlines():
        new_line = line
        for key in CALIB_FLAGS_TO_FREEZE:
            pattern = rf"^(\s*{re.escape(key)}\s*:\s*)(true|false)(.*)$"
            match = re.match(pattern, line)
            if match:
                prefix, _old_value, suffix = match.groups()
                new_line = f"{prefix}false{suffix}"
                counts[key] += 1
                break
        lines.append(new_line)

    return "\n".join(lines) + "\n", counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Freeze OpenVINS online camera calibration flags.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    text = args.input.read_text()
    frozen_text, counts = freeze_calibration_text(text)

    missing = [key for key, count in counts.items() if count != 1]
    if missing:
        print(f"ERROR: expected exactly one occurrence for each flag, bad counts: {counts}")
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(frozen_text)

    print(f"input: {args.input}")
    print(f"output: {args.output}")
    for key in CALIB_FLAGS_TO_FREEZE:
        print(f"{key}: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
