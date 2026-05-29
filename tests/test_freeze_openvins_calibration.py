import importlib.util
from pathlib import Path


def load_script_module():
    script_path = Path("scripts/freeze_openvins_calibration.py").resolve()
    spec = importlib.util.spec_from_file_location("freeze_openvins_calibration_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_freeze_calibration_text_sets_three_camera_flags_false():
    module = load_script_module()

    text = """verbosity: INFO
calib_cam_extrinsics: true # optimize extrinsics
calib_cam_intrinsics: true # optimize intrinsics
calib_cam_timeoffset: true # optimize timing
calib_imu_intrinsics: false # leave unchanged
"""

    frozen, counts = module.freeze_calibration_text(text)

    assert counts["calib_cam_extrinsics"] == 1
    assert counts["calib_cam_intrinsics"] == 1
    assert counts["calib_cam_timeoffset"] == 1
    assert "calib_cam_extrinsics: false # optimize extrinsics" in frozen
    assert "calib_cam_intrinsics: false # optimize intrinsics" in frozen
    assert "calib_cam_timeoffset: false # optimize timing" in frozen
    assert "calib_imu_intrinsics: false # leave unchanged" in frozen
