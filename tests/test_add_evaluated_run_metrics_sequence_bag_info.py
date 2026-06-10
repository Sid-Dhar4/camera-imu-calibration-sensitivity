import importlib.util
from pathlib import Path


def load_script_module():
    script_path = Path("scripts/add_evaluated_run_metrics_row.py").resolve()
    spec = importlib.util.spec_from_file_location("add_evaluated_run_metrics_row_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parse_bag_duration_reads_duration():
    module = load_script_module()
    path = Path("results/logs/setup/MH_03_medium_ros2_bag_info.txt")
    duration = module.parse_bag_duration(path)

    assert duration is not None
    assert duration > 100.0
