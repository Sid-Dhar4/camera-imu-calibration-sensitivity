import importlib.util
from pathlib import Path

import numpy as np


def load_script_module():
    script_path = Path("scripts/plot_aligned_tum_trajectories.py").resolve()
    spec = importlib.util.spec_from_file_location("plot_aligned_tum_trajectories_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_align_se3_no_scale_recovers_translated_points():
    module = load_script_module()

    source = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [3.0, 0.0, 0.0],
    ])
    target = source + np.array([5.0, -2.0, 1.0])

    aligned = module.align_se3_no_scale(source, target)

    assert np.allclose(aligned, target)


def test_associate_by_time_keeps_close_pairs():
    module = load_script_module()

    ref_t = np.array([0.0, 1.0, 2.0])
    ref_xyz = np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0]], dtype=float)
    est_t = np.array([0.01, 1.02, 3.00])
    est_xyz = np.array([[0, 0, 0], [1, 0, 0], [3, 0, 0]], dtype=float)

    ref_out, est_out = module.associate_by_time(ref_t, ref_xyz, est_t, est_xyz, max_dt=0.05)

    assert len(ref_out) == 2
    assert len(est_out) == 2
