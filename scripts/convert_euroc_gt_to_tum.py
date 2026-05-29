#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path


def find_column(fieldnames, candidates):
    normalized = {name.strip().lstrip("#").strip(): name for name in fieldnames}
    for c in candidates:
        if c in normalized:
            return normalized[c]
    raise KeyError(f"Could not find any of columns: {candidates}")


def convert_euroc_gt_to_tum(input_path: Path, output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = 0

    with input_path.open("r", newline="") as fin, output_path.open("w") as fout:
        reader = csv.DictReader(fin)
        if reader.fieldnames is None:
            raise RuntimeError("CSV has no header")

        t_col = find_column(reader.fieldnames, ["timestamp", "timestamp [ns]"])
        px_col = find_column(reader.fieldnames, ["p_RS_R_x [m]", "p_RS_R_x"])
        py_col = find_column(reader.fieldnames, ["p_RS_R_y [m]", "p_RS_R_y"])
        pz_col = find_column(reader.fieldnames, ["p_RS_R_z [m]", "p_RS_R_z"])
        qw_col = find_column(reader.fieldnames, ["q_RS_w []", "q_RS_w"])
        qx_col = find_column(reader.fieldnames, ["q_RS_x []", "q_RS_x"])
        qy_col = find_column(reader.fieldnames, ["q_RS_y []", "q_RS_y"])
        qz_col = find_column(reader.fieldnames, ["q_RS_z []", "q_RS_z"])

        for row in reader:
            timestamp_s = float(row[t_col]) * 1e-9
            tx = float(row[px_col])
            ty = float(row[py_col])
            tz = float(row[pz_col])
            qw = float(row[qw_col])
            qx = float(row[qx_col])
            qy = float(row[qy_col])
            qz = float(row[qz_col])
            fout.write(f"{timestamp_s:.9f} {tx:.9f} {ty:.9f} {tz:.9f} {qx:.9f} {qy:.9f} {qz:.9f} {qw:.9f}\n")
            rows += 1

    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert EuRoC ground truth CSV to TUM trajectory format.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    rows = convert_euroc_gt_to_tum(args.input, args.output)
    print(f"input: {args.input}")
    print(f"output: {args.output}")
    print(f"tum_rows: {rows}")
    if rows == 0:
        print("ERROR: no rows written")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
