import importlib.util
from pathlib import Path


def load_script_module():
    script_path = Path("scripts/generate_rotation_sweep_configs.py").resolve()
    spec = importlib.util.spec_from_file_location("generate_rotation_sweep_configs_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_magnitude_label_formats_sweep_directory_labels():
    module = load_script_module()

    assert module.magnitude_label(0.5) == "0p5"
    assert module.magnitude_label(1.0) == "1"
    assert module.magnitude_label(2.0) == "2"
    assert module.magnitude_label(5.0) == "5"
