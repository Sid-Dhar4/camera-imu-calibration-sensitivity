#!/usr/bin/env python3
import json
import re
from pathlib import Path


def parse_rmse(path: Path):
    text = path.read_text()
    match = re.search(r"^\s*rmse\s+([0-9eE+\-.]+)", text, re.MULTILINE)
    if not match:
        return None
    return float(match.group(1))


def main() -> int:
    run_id = "openvins_MH01_nominal_full_000"
    evo_dir = Path("results") / "evo" / run_id

    summary = {
        "run_id": run_id,
        "sequence": "MH_01_easy",
        "backend": "openvins",
        "alignment": "SE3_no_scale",
        "t_max_diff_s": 0.01,
        "ate_rmse_m": parse_rmse(evo_dir / "ape_console.txt"),
        "rpe_trans_rmse_m": parse_rmse(evo_dir / "rpe_trans_console.txt"),
        "rpe_rot_rmse_deg": parse_rmse(evo_dir / "rpe_rot_console.txt"),
    }

    out = evo_dir / "evo_summary.json"
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    missing = [k for k, v in summary.items() if k.endswith("_m") or k.endswith("_deg") if v is None]
    if missing:
        print(f"ERROR: missing parsed metrics: {missing}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
