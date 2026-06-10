#!/usr/bin/env python3
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def load_tum_positions(path: Path) -> tuple[np.ndarray, np.ndarray]:
    timestamps = []
    positions = []

    with path.open() as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 8:
                continue
            timestamps.append(float(parts[0]))
            positions.append([float(parts[1]), float(parts[2]), float(parts[3])])

    if not timestamps:
        raise ValueError(f"no TUM poses found in {path}")

    return np.asarray(timestamps), np.asarray(positions)


def associate_by_time(
    ref_t: np.ndarray,
    ref_xyz: np.ndarray,
    est_t: np.ndarray,
    est_xyz: np.ndarray,
    max_dt: float,
) -> tuple[np.ndarray, np.ndarray]:
    ref_out = []
    est_out = []

    j = 0
    for t, xyz in zip(est_t, est_xyz):
        while j + 1 < len(ref_t) and abs(ref_t[j + 1] - t) <= abs(ref_t[j] - t):
            j += 1

        if abs(ref_t[j] - t) <= max_dt:
            ref_out.append(ref_xyz[j])
            est_out.append(xyz)

    if not ref_out:
        raise ValueError("no associated trajectory pairs found")

    return np.asarray(ref_out), np.asarray(est_out)


def align_se3_no_scale(source_xyz: np.ndarray, target_xyz: np.ndarray) -> np.ndarray:
    source_mean = source_xyz.mean(axis=0)
    target_mean = target_xyz.mean(axis=0)

    source_centered = source_xyz - source_mean
    target_centered = target_xyz - target_mean

    h = source_centered.T @ target_centered
    u, _s, vt = np.linalg.svd(h)
    r = vt.T @ u.T

    if np.linalg.det(r) < 0:
        vt[-1, :] *= -1
        r = vt.T @ u.T

    t = target_mean - r @ source_mean
    return (r @ source_xyz.T).T + t


def plot_plane(
    trajectories: list[tuple[str, np.ndarray]],
    plane: str,
    output: Path,
    title: str,
) -> None:
    axis_map = {
        "xy": (0, 1, "x (m)", "y (m)"),
        "xz": (0, 2, "x (m)", "z (m)"),
        "yz": (1, 2, "y (m)", "z (m)"),
    }
    if plane not in axis_map:
        raise ValueError(f"unsupported plane: {plane}")

    i, j, xlabel, ylabel = axis_map[plane]

    plt.figure()
    for label, xyz in trajectories:
        plt.plot(xyz[:, i], xyz[:, j], label=label)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.axis("equal")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=180)
    plt.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot SE(3)-aligned TUM trajectories against ground truth.")
    parser.add_argument("--groundtruth", required=True, type=Path)
    parser.add_argument("--estimate", required=True, action="append", nargs=2, metavar=("LABEL", "PATH"))
    parser.add_argument("--output-prefix", required=True, type=Path)
    parser.add_argument("--max-dt", default=0.01, type=float)
    args = parser.parse_args()

    ref_t, ref_xyz = load_tum_positions(args.groundtruth)

    trajectories = []
    ref_for_plot = None
    association_counts = {}

    for label, est_path_str in args.estimate:
        est_path = Path(est_path_str)
        est_t, est_xyz = load_tum_positions(est_path)
        ref_assoc, est_assoc = associate_by_time(ref_t, ref_xyz, est_t, est_xyz, max_dt=args.max_dt)
        est_aligned = align_se3_no_scale(est_assoc, ref_assoc)

        if ref_for_plot is None:
            ref_for_plot = ref_assoc

        trajectories.append((label, est_aligned))
        association_counts[label] = int(len(est_aligned))

    if ref_for_plot is None:
        raise ValueError("no estimates provided")

    all_trajectories = [("ground truth", ref_for_plot)] + trajectories

    xy_path = args.output_prefix.with_name(args.output_prefix.name + "_xy.png")
    xz_path = args.output_prefix.with_name(args.output_prefix.name + "_xz.png")

    plot_plane(all_trajectories, "xy", xy_path, "MH_01_easy aligned trajectory comparison (XY)")
    plot_plane(all_trajectories, "xz", xz_path, "MH_01_easy aligned trajectory comparison (XZ)")

    print(f"wrote {xy_path}")
    print(f"wrote {xz_path}")
    for label, count in association_counts.items():
        print(f"associated_pairs[{label}]: {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
