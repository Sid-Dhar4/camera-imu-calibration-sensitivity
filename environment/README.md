# Environment Notes

This repo separates two environments:

1. Host Python environment:
   - automation scripts
   - metrics aggregation
   - plotting
   - evo evaluation

2. OpenVINS runtime environment:
   - reused from the existing VIO/SLAM benchmark when possible
   - otherwise Docker-based for reproducibility

The MVP should not depend on native ROS 2 Jazzy OpenVINS unless it is proven locally.
