import importlib.util
from pathlib import Path


def load_script_module():
    script_path = Path("scripts/summarize_multisequence_rot5.py").resolve()
    spec = importlib.util.spec_from_file_location("summarize_multisequence_rot5_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_build_summary_includes_mh01_and_mh03():
    module = load_script_module()
    rows = module.read_metrics(Path("results/metrics.csv"))
    summary = module.build_summary(rows)

    sequences = {row["sequence"] for row in summary}
    assert sequences == {"MH_01_easy", "MH_03_medium"}

    mh03 = next(row for row in summary if row["sequence"] == "MH_03_medium")
    assert mh03["rotation_z_5deg_ate_rmse_m"] > mh03["nominal_ate_rmse_m"]
