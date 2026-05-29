import importlib.util
from pathlib import Path


def load_script_module():
    script_path = Path("scripts/perturb_extrinsics.py").resolve()
    spec = importlib.util.spec_from_file_location("perturb_extrinsics_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_perturb_imucam_yaml_text_row_list_format_counts_two_matrices():
    module = load_script_module()

    text = """%YAML:1.0

cam0:
  T_imu_cam:
    - [1.0, 0.0, 0.0, 0.1]
    - [0.0, 1.0, 0.0, 0.2]
    - [0.0, 0.0, 1.0, 0.3]
    - [0.0, 0.0, 0.0, 1.0]
  rostopic: /cam0/image_raw
cam1:
  T_imu_cam:
    - [1.0, 0.0, 0.0, -0.1]
    - [0.0, 1.0, 0.0, -0.2]
    - [0.0, 0.0, 1.0, -0.3]
    - [0.0, 0.0, 0.0, 1.0]
  rostopic: /cam1/image_raw
"""

    out, count = module.perturb_imucam_yaml_text(text, axis="z", angle_deg=5.0)

    assert count == 2
    assert "T_imu_cam" in out
    assert "rostopic: /cam0/image_raw" in out
    assert "rostopic: /cam1/image_raw" in out
    assert "0.1]" in out or "0.1" in out
    assert "-0.1]" in out or "-0.1" in out
