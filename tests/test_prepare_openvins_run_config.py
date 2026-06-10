import importlib.util
from pathlib import Path


def load_script_module():
    script_path = Path("scripts/prepare_openvins_run_config.py").resolve()
    spec = importlib.util.spec_from_file_location("prepare_openvins_run_config_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_replace_required_replaces_existing_pattern():
    module = load_script_module()

    assert module.replace_required("a: false\n", "a: false", "a: true") == "a: true\n"


def test_replace_required_raises_for_missing_pattern():
    module = load_script_module()

    try:
        module.replace_required("a: false\n", "b: false", "b: true")
    except ValueError as exc:
        assert "required pattern not found" in str(exc)
    else:
        raise AssertionError("expected ValueError")
