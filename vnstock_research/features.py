from __future__ import annotations

import numpy as np
import pandas as pd


FEATURE_COLUMNS = ["ret_5", "ret_20", "vol_20", "volume_z_20", "range_20", "trend_20"]


def build_daily_features(bars: pd.DataFrame) -> pd.DataFrame:
    out = bars.sort_values(["symbol", "date"]).copy()
    g = out.groupby("symbol", group_keys=False)
    out["ret_1"] = g["close"].pct_change()
    out["ret_5"] = g["close"].pct_change(5)
    out["ret_20"] = g["close"].pct_change(20)
    out["vol_20"] = g["ret_1"].transform(lambda s: s.rolling(20, min_periods=20).std() * np.sqrt(252))
    log_volume = np.log1p(out["volume"])
    out["volume_z_20"] = g["volume"].transform(lambda s: (np.log1p(s) - np.log1p(s).rolling(20, min_periods=20).mean()) / np.log1p(s).rolling(20, min_periods=20).std())
    out["range_20"] = g.apply(lambda x: (x["high"] / x["low"] - 1).rolling(20, min_periods=20).mean()).reset_index(level=0, drop=True)
    out["trend_20"] = g["close"].transform(lambda s: s.rolling(20, min_periods=20).apply(lambda x: np.polyfit(np.arange(len(x)), np.log(x), 1)[0], raw=True))
    out = out.replace([np.inf, -np.inf], np.nan)
    return out


def make_stock_windows(features: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    rows = []
    for symbol, group in features.sort_values(["symbol", "date"]).groupby("symbol"):
        group = group.reset_index(drop=True)
        for end in range(window - 1, len(group)):
            sample = group.iloc[end - window + 1 : end + 1]
            if sample[FEATURE_COLUMNS].isna().any().any():
                continue
            row = {"symbol": symbol, "as_of": group.loc[end, "date"]}
            for col in FEATURE_COLUMNS:
                row[f"{col}_mean"] = float(sample[col].mean())
                row[f"{col}_last"] = float(sample[col].iloc[-1])
            rows.append(row)
    return pd.DataFrame(rows)


def add_forward_returns(windows: pd.DataFrame, bars: pd.DataFrame, horizons=(1, 5, 10)) -> pd.DataFrame:
    price = bars.pivot(index="date", columns="symbol", values="close").sort_index()
    out = windows.copy()
    for h in horizons:
        vals = []
        for _, row in out.iterrows():
            try:
                i = price.index.get_loc(pd.Timestamp(row["as_of"]))
                if i + h >= len(price.index):
                    vals.append(np.nan)
                else:
                    p0 = price.loc[price.index[i], row["symbol"]]
                    p1 = price.loc[price.index[i + h], row["symbol"]]
                    vals.append(float(p1 / p0 - 1))
            except (KeyError, IndexError):
                vals.append(np.nan)
        out[f"fwd_{h}d"] = vals
    return out

