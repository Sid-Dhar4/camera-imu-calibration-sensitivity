from metrics.schema import REQUIRED_COLUMNS, ALLOWED_STATUS, ALLOWED_PERTURB_TYPES


def test_required_metrics_columns_are_stable():
    assert REQUIRED_COLUMNS[0] == "run_id"
    assert REQUIRED_COLUMNS[-1] == "notes"
    assert len(REQUIRED_COLUMNS) == 18


def test_allowed_status_values():
    assert "success" in ALLOWED_STATUS
    assert "tracking_lost" in ALLOWED_STATUS
    assert "eval_failed" in ALLOWED_STATUS


def test_allowed_perturbation_types():
    assert {"nominal", "rotation", "translation", "timestamp"} <= ALLOWED_PERTURB_TYPES
