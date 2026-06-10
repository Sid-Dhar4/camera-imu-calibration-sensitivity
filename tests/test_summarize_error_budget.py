import importlib.util
from pathlib import Path


def load_script_module():
    script_path = Path("scripts/summarize_error_budget.py").resolve()
    spec = importlib.util.spec_from_file_location("summarize_error_budget_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_collect_error_budget_rows_keeps_expected_rows():
    module = load_script_module()
    rows = module.collect_error_budget_rows(Path("results/metrics.csv"), "MH_01_easy")
    labels = {row["label"] for row in rows}

    assert "nominal" in labels
    assert "rotation_z_5.0deg" in labels
    assert "translation_y_1.0cm" in labels
    assert "translation_y_2.0cm" in labels
    assert "translation_y_5.0cm" in labels
