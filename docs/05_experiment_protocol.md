# Experiment Protocol

EXP-001 Behavioral Clustering:

1. Validate and fingerprint raw OHLCV.
2. Compute daily returns, rolling volatility, volume z-score, range, and trend.
3. Build a trailing stock-window vector; drop only rows whose required trailing history is unavailable.
4. Attach forward returns from dates strictly after the feature date.
5. Split by date into train, validation, and test. Never random-shuffle windows.
6. Fit scaler/PCA/clustering on train only in the production implementation; use the same fitted transform on validation/test.
7. Report cluster sizes, descriptive features, forward-return distributions, hit rate, drawdown, turnover, and costs.
8. Compare to unconditional, sector, market-regime, and naive momentum baselines.

The current compact skeleton demonstrates the flow and artifact contract. Before claiming production research results, refactor the fit/evaluate boundary so clustering is explicitly re-fit per walk-forward fold and add costs/liquidity.

