from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

from .clustering import cluster_windows, transform_windows
from .data import frame_fingerprint, validate_bars
from .evaluation import evaluate_walk_forward, summarize_forward_returns, walk_forward_splits
from .features import add_forward_returns, build_daily_features, make_stock_windows


def run_exp_001(bars: pd.DataFrame, output_dir: str | Path, *, n_clusters: int = 3, method: str = "kmeans", window: int = 20, pca_components: int = 0) -> dict:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    bars = validate_bars(bars)
    features = build_daily_features(bars)
    windows = make_stock_windows(features, window=window)
    windows = add_forward_returns(windows, bars)
    clustered, model_info = cluster_windows(windows, n_clusters=n_clusters, method=method, pca_components=pca_components)
    # Descriptive labels are retained for the full sample, but reported test metrics
    # are generated from a transform fitted only on each training fold.
    fold_reports = []
    for train, validation, test in walk_forward_splits(windows):
        fit_train, fold_model = cluster_windows(train, n_clusters=n_clusters, method=method, pca_components=pca_components)
        try:
            fold_test = transform_windows(test, fold_model)
            fold_reports.append({"train_rows": len(fit_train), "validation_rows": len(validation), "test_rows": len(fold_test), "test_summary": summarize_forward_returns(fold_test)})
        except ValueError:
            fold_reports.append({"train_rows": len(fit_train), "validation_rows": len(validation), "test_rows": 0, "test_summary": {}, "note": "model has no out-of-sample transform"})
    metrics = {"splits": fold_reports}
    report = {
        "experiment_id": "EXP-001",
        "name": "Behavioral Clustering",
        "config": {"n_clusters": n_clusters, "method": method, "window": window, "pca_components": pca_components},
        "dataset_fingerprint": frame_fingerprint(bars),
        "rows": {"bars": len(bars), "windows": len(clustered)},
        "feature_columns": model_info["feature_cols"],
        "metrics": metrics,
        "limitations": ["Synthetic or point-in-time-clean data is required for production conclusions.", "Cluster labels are descriptive and not alpha by themselves.", "No transaction costs, slippage, fees, halts, or liquidity constraints are modeled yet."],
    }
    clustered.to_csv(output / "clustered_windows.csv", index=False)
    features.to_csv(output / "daily_features.csv", index=False)
    (output / "report.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    return report
