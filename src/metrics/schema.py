REQUIRED_COLUMNS = [
    "run_id",
    "sequence",
    "backend",
    "perturb_type",
    "perturb_axis",
    "perturb_magnitude",
    "perturb_units",
    "config_path",
    "trajectory_path",
    "status",
    "ate_rmse_m",
    "rpe_trans_rmse_m",
    "rpe_rot_rmse_deg",
    "runtime_s",
    "estimated_duration_s",
    "completion_rate",
    "failure_reason",
    "notes",
]

ALLOWED_STATUS = {
    "success",
    "partial",
    "init_failed",
    "tracking_lost",
    "trajectory_missing",
    "runtime_error",
    "eval_failed",
}

ALLOWED_PERTURB_TYPES = {
    "nominal",
    "rotation",
    "translation",
    "timestamp",
}
