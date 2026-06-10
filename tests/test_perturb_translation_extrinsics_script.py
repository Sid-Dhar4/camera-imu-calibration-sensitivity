import importlib.util
from pathlib import Path


def load_script_module():
    script_path = Path("scripts/perturb_translation_extrinsics.py").resolve()
    spec = importlib.util.spec_from_file_location("perturb_translation_extrinsics_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_translation_script_perturbs_two_row_list_matrices():
    module = load_script_module()
    text = """cam0:
  T_imu_cam:
    - [1, 0, 0, 0.1]
    - [0, 1, 0, 0.2]
    - [0, 0, 1, 0.3]
    - [0, 0, 0, 1]
cam1:
  T_imu_cam:
    - [1, 0, 0, 1.1]
    - [0, 1, 0, 1.2]
    - [0, 0, 1, 1.3]
    - [0, 0, 0, 1]
"""

    out, count = module.perturb_imucam_yaml_translation_text(text, axis="y", magnitude_m=0.05)

    assert count == 2
    assert "- [0, 1, 0, 0.25]" in out
    assert "- [0, 1, 0, 1.25]" in out
