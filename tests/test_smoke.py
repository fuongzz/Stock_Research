from pathlib import Path
import json
from vnstock_research.data import make_synthetic_bars, validate_bars
from vnstock_research.features import build_daily_features, make_stock_windows, add_forward_returns
from vnstock_research.experiment import run_exp_001


def test_pipeline_smoke(tmp_path: Path):
    bars = validate_bars(make_synthetic_bars(periods=180))
    features = build_daily_features(bars)
    windows = add_forward_returns(make_stock_windows(features), bars)
    assert len(windows) > 0
    report = run_exp_001(bars, tmp_path)
    assert report["experiment_id"] == "EXP-001"
    assert (tmp_path / "report.json").exists()
    assert json.loads((tmp_path / "report.json").read_text())["dataset_fingerprint"]

