#!/usr/bin/env python3
import argparse
from pathlib import Path


def convert_openvins_state_to_tum(input_path: Path, output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = 0

    with input_path.open("r") as fin, output_path.open("w") as fout:
        for line in fin:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            if len(parts) < 8:
                continue

            timestamp = float(parts[0])

            # OpenVINS saved state columns:
            # timestamp qx qy qz qw px py pz ...
            qx = float(parts[1])
            qy = float(parts[2])
            qz = float(parts[3])
            qw = float(parts[4])
            tx = float(parts[5])
            ty = float(parts[6])
            tz = float(parts[7])

            fout.write(f"{timestamp:.9f} {tx:.9f} {ty:.9f} {tz:.9f} {qx:.9f} {qy:.9f} {qz:.9f} {qw:.9f}\n")
            rows += 1

    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert OpenVINS saved state output to TUM trajectory format.")
    parser.add_argument("--input", required=True, type=Path, help="Path to OpenVINS ov_estimate.txt")
    parser.add_argument("--output", required=True, type=Path, help="Output TUM trajectory path")
    args = parser.parse_args()

    rows = convert_openvins_state_to_tum(args.input, args.output)
    print(f"input: {args.input}")
    print(f"output: {args.output}")
    print(f"tum_rows: {rows}")
    if rows == 0:
        print("ERROR: no trajectory rows were written")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
