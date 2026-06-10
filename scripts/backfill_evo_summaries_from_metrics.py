#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path


def run_group(row: dict) -> str:
    return "nominal" if row["perturb_type"] == "nominal" else "perturbed"


def make_summary(row: dict) -> dict:
    return {
        "ate_rmse_m": float(row["ate_rmse_m"]),
        "rpe_trans_rmse_m": float(row["rpe_trans_rmse_m"]),
        "rpe_rot_rmse_deg": float(row["rpe_rot_rmse_deg"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create lightweight evo_summary.json files from results/metrics.csv.")
    parser.add_argument("--metrics", default="results/metrics.csv")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    with Path(args.metrics).open(newline="") as f:
        rows = list(csv.DictReader(f))

    written = []
    skipped = []
    for row in rows:
        group = run_group(row)
        run_id = row["run_id"]
        out = Path("results/evo") / group / run_id / "evo_summary.json"
        if out.exists() and not args.overwrite:
            skipped.append(str(out))
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(make_summary(row), indent=2) + "\n")
        written.append(str(out))

    print(f"written: {len(written)}")
    for path in written:
        print(path)
    print(f"skipped_existing: {len(skipped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
