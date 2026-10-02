# Hypothesis Protocol

1. Register one falsifiable statement before inspecting test results.
2. Define population, eligible dates, feature availability, horizon, benchmark, costs, and exclusion rules.
3. Define the primary metric and one or more failure thresholds.
4. Freeze the dataset snapshot and code version.
5. Run baseline, ablation, and robustness checks.
6. Record every attempted variant, including failures.
7. Promote an alpha only after independent validation and review.

Example:

> Within the point-in-time eligible VN30 universe, windows in the high-momentum/low-volatility cluster have higher 10-session excess returns than the universe median during neutral-to-bullish regimes.

Falsification: no positive difference after costs in the untouched test period, or instability across at least two regime partitions.

