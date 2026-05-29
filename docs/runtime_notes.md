# Runtime Notes

## Python test runner

Use:

```bash
./scripts/run_tests.sh
```

This disables external pytest plugin autoload so ROS 2 launch_testing plugins do not contaminate this repo test suite.

## evo note

Do not verify evo with bare `evo_ape --version`, because evo_ape expects a subcommand such as `tum`, `euroc`, `bag`, or `bag2`.

Use `python -m pip show evo` and `evo_ape -h` for smoke verification.

## Docker note

Docker exists on this machine, but the current user did not have Docker daemon access during discovery. Avoid Docker unless access is fixed or sudo workflow is intentionally chosen.
