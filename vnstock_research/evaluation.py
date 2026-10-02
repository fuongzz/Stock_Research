from __future__ import annotations

import numpy as np
import pandas as pd


def walk_forward_splits(frame: pd.DataFrame, date_col: str = "as_of", train_fraction: float = 0.6, validation_fraction: float = 0.2):
    dates = sorted(pd.to_datetime(frame[date_col]).unique())
    n = len(dates)
    train_end = max(1, int(n * train_fraction))
    val_end = max(train_end + 1, int(n * (train_fraction + validation_fraction)))
    return [(frame[frame[date_col].isin(dates[:train_end])], frame[frame[date_col].isin(dates[train_end:val_end])], frame[frame[date_col].isin(dates[val_end:])])]


def summarize_forward_returns(frame: pd.DataFrame, return_cols=("fwd_1d", "fwd_5d", "fwd_10d")) -> dict:
    report = {}
    for cluster_id, group in frame.groupby("cluster_id"):
        item = {"n": int(len(group))}
        for col in return_cols:
            s = group[col].dropna()
            item[col] = {"mean": float(s.mean()) if len(s) else None, "median": float(s.median()) if len(s) else None, "hit_rate": float((s > 0).mean()) if len(s) else None}
        report[str(int(cluster_id))] = item
    return report


def evaluate_walk_forward(frame: pd.DataFrame, return_cols=("fwd_1d", "fwd_5d", "fwd_10d")) -> dict:
    splits = walk_forward_splits(frame)
    return {"splits": [{"train_rows": len(tr), "validation_rows": len(va), "test_rows": len(te), "test_summary": summarize_forward_returns(te, return_cols)} for tr, va, te in splits]}
