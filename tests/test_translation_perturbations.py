import numpy as np

from calibration_perturb.transforms import perturb_T_imu_cam_translation_imu_frame


def test_translation_perturbation_adds_y_translation_only():
    T = np.eye(4)
    T[0, 3] = 1.0
    T[1, 3] = 2.0
    T[2, 3] = 3.0

    T_new = perturb_T_imu_cam_translation_imu_frame(T, axis="y", magnitude_m=0.05)

    assert np.allclose(T_new[:3, 3], [1.0, 2.05, 3.0])
    assert np.allclose(T_new[:3, :3], np.eye(3))


def test_translation_perturbation_rejects_bad_axis():
    T = np.eye(4)
    try:
        perturb_T_imu_cam_translation_imu_frame(T, axis="bad", magnitude_m=0.01)
    except ValueError as exc:
        assert "Unsupported axis" in str(exc)
    else:
        raise AssertionError("expected ValueError")
