# Architecture

```text
nominal OpenVINS config
        |
        v
perturb config generator
        |
        v
generated OpenVINS config
        |
        v
run OpenVINS on EuRoC
        |
        v
trajectory output
        |
        v
evo ATE/RPE evaluation
        |
        v
results/metrics.csv
        |
        v
plots + calibration_error_budget.md
```
