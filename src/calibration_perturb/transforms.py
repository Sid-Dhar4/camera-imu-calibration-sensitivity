from __future__ import annotations

import math
import numpy as np


def axis_angle_to_rotation_matrix(axis: str, angle_deg: float) -> np.ndarray:
    axis = axis.lower()
    angle_rad = math.radians(angle_deg)
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)

    if axis == "x":
        return np.array([[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]], dtype=float)
    if axis == "y":
        return np.array([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]], dtype=float)
    if axis == "z":
        return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]], dtype=float)

    raise ValueError(f"Unsupported axis: {axis}. Use x, y, or z.")


def make_transform(matrix_flat_row_major: list[float]) -> np.ndarray:
    if len(matrix_flat_row_major) != 16:
        raise ValueError(f"Expected 16 values for 4x4 transform, got {len(matrix_flat_row_major)}")
    return np.array(matrix_flat_row_major, dtype=float).reshape((4, 4))


def flatten_transform(T: np.ndarray) -> list[float]:
    if T.shape != (4, 4):
        raise ValueError(f"Expected 4x4 transform, got {T.shape}")
    return [float(x) for x in T.reshape(-1)]


def perturb_T_imu_cam_rotation_left(T_imu_cam: np.ndarray, axis: str, angle_deg: float) -> np.ndarray:
    if T_imu_cam.shape != (4, 4):
        raise ValueError(f"Expected 4x4 transform, got {T_imu_cam.shape}")

    T_new = T_imu_cam.copy()
    R_delta = axis_angle_to_rotation_matrix(axis, angle_deg)
    T_new[:3, :3] = R_delta @ T_imu_cam[:3, :3]
    T_new[:3, 3] = T_imu_cam[:3, 3]
    T_new[3, :] = np.array([0.0, 0.0, 0.0, 1.0])
    return T_new


def rotation_angle_between(R_a: np.ndarray, R_b: np.ndarray) -> float:
    R = R_a @ R_b.T
    cos_angle = (np.trace(R) - 1.0) / 2.0
    cos_angle = max(-1.0, min(1.0, float(cos_angle)))
    return math.degrees(math.acos(cos_angle))
