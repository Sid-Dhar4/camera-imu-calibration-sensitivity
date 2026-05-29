# EuRoC Bag Preparation

Date: 2026-05-28

## Source data

Existing ROS 1 EuRoC bags are stored outside the repo:

```text
~/datasets/euroc/bags/MH_01_easy.bag
~/datasets/euroc/bags/MH_03_medium.bag
~/datasets/euroc/bags/MH_05_difficult.bag
```

## ROS 2 conversion

Use:

```bash
source .venv/bin/activate
scripts/convert_euroc_ros1_to_ros2.sh ~/datasets/euroc/bags/MH_01_easy.bag ~/datasets/euroc/ros2_bags/MH_01_easy
```

The converted ROS 2 bag is stored outside the repo:

```text
~/datasets/euroc/ros2_bags/MH_01_easy
```

## Why bags are outside the repo

EuRoC bags are large binary data files. The repo stores scripts and logs, not dataset binaries.

## Verification artifact

Converted bag metadata is saved in:

```text
results/logs/setup/MH_01_easy_ros2_bag_info.txt
```
