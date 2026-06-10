import importlib.util
from pathlib import Path


def load_script_module():
    script_path = Path("scripts/prepare_openvins_run_config.py").resolve()
    spec = importlib.util.spec_from_file_location("prepare_openvins_run_config_script", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_nominal_run_uses_nominal_output_group(tmp_path):
    module = load_script_module()

    run_id = "test_nominal_group"
    source_config_dir = Path("configs/nominal/openvins/euroc_mav")

    module.prepare_run_config(
        run_id=run_id,
        source_config_dir=source_config_dir,
        output_root=tmp_path / "configs_used",
        log_root=tmp_path / "logs",
        trajectory_root=tmp_path / "trajectories",
        evo_root=tmp_path / "evo",
        perturb_type="nominal",
        perturb_axis="none",
        perturb_magnitude="0",
        perturb_units="none",
        sequence="MH_03_medium",
    )

    assert (tmp_path / "logs" / "nominal" / run_id / "run_metadata.yaml").exists()
    assert not (tmp_path / "logs" / "perturbed" / run_id).exists()

    cfg = (tmp_path / "configs_used" / run_id / "estimator_config.yaml").read_text()
    assert "trajectories/nominal/test_nominal_group/ov_estimate.txt" in cfg
