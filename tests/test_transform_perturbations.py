import numpy as np

from calibration_perturb.transforms import (
    axis_angle_to_rotation_matrix,
    make_transform,
    perturb_T_imu_cam_rotation_left,
    rotation_angle_between,
)


def test_axis_angle_z_90_degrees():
    R = axis_angle_to_rotation_matrix("z", 90.0)
    expected = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    assert np.allclose(R, expected, atol=1e-9)


def test_rotation_perturbation_preserves_translation():
    T = np.eye(4)
    T[:3, 3] = np.array([0.1, -0.2, 0.3])
    T_new = perturb_T_imu_cam_rotation_left(T, "z", 5.0)
    assert np.allclose(T_new[:3, 3], T[:3, 3])
    assert np.allclose(T_new[3, :], np.array([0.0, 0.0, 0.0, 1.0]))


def test_rotation_perturbation_angle_is_requested_angle():
    T = np.eye(4)
    T_new = perturb_T_imu_cam_rotation_left(T, "z", 5.0)
    angle = rotation_angle_between(T_new[:3, :3], T[:3, :3])
    assert abs(angle - 5.0) < 1e-9


def test_make_transform_requires_16_values():
    T = make_transform(list(range(16)))
    assert T.shape == (4, 4)
