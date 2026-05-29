# Docker Notes

Docker will be used only if the existing OpenVINS environment is not reusable.

Preferred MVP order:
1. Reuse known working OpenVINS EuRoC setup from the VIO/SLAM benchmark.
2. If unavailable, build an isolated OpenVINS container.
3. Avoid changing the host ROS 2 Jazzy installation unless necessary.
