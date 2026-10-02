from __future__ import annotations

import hashlib
from typing import Iterable
import numpy as np
import pandas as pd


REQUIRED = ["symbol", "date", "open", "high", "low", "close", "volume"]


def validate_bars(bars: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED if c not in bars.columns]
    if missing:
        raise ValueError(f"Missing OHLCV columns: {missing}")
    out = bars.copy()
    out["date"] = pd.to_datetime(out["date"], utc=False).dt.normalize()
    out = out.sort_values(["symbol", "date"]).drop_duplicates(["symbol", "date"])
    if out["close"].isna().any() or (out["close"] <= 0).any():
        raise ValueError("close must be positive and non-null")
    if (out["volume"] < 0).any():
        raise ValueError("volume cannot be negative")
    return out.reset_index(drop=True)


def frame_fingerprint(frame: pd.DataFrame) -> str:
    cols = [c for c in ["symbol", "date", "close", "volume"] if c in frame]
    payload = pd.util.hash_pandas_object(frame[cols].sort_values(cols), index=False).values.tobytes()
    return hashlib.sha256(payload).hexdigest()[:16]


def make_synthetic_bars(symbols: Iterable[str] = ("AAA", "BBB", "CCC", "DDD"), periods: int = 520, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2022-01-03", periods=periods)
    rows = []
    for idx, symbol in enumerate(symbols):
        drift = (idx - 1.5) * 0.00015
        vol = 0.008 + idx * 0.002
        shocks = rng.normal(drift, vol, len(dates))
        close = 100 * np.exp(np.cumsum(shocks))
        open_ = close * (1 + rng.normal(0, vol / 3, len(dates)))
        high = np.maximum(open_, close) * (1 + rng.uniform(0, vol, len(dates)))
        low = np.minimum(open_, close) * (1 - rng.uniform(0, vol, len(dates)))
        volume = rng.lognormal(12 + idx * 0.1, 0.35, len(dates))
        rows.extend(zip([symbol] * len(dates), dates, open_, high, low, close, volume))
    return pd.DataFrame(rows, columns=REQUIRED)

