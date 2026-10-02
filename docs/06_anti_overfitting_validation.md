# Anti-Overfitting and Leakage Controls

- Use time-ordered train/validation/test splits and embargo overlapping labels.
- Fit scalers, PCA, clusters, regime models, and feature-selection steps inside each training fold.
- Preserve delisted names and point-in-time universe membership; never use today's surviving list for history.
- Use adjusted prices consistently and version corporate-action processing.
- Include fees, taxes, spread, slippage, price limits, halts, lot constraints, and liquidity caps in portfolio tests.
- Keep a research ledger of all trials; control multiple testing with a holdout, false-discovery procedure, or deflated performance statistic.
- Require stability across symbols, sectors, regimes, subperiods, and perturbations.
- Prefer economically interpretable features and penalize turnover.
- Use placebo tests, label-shuffling, and feature-timing audits.
- Do not let an LLM select or alter metrics after seeing test outcomes.

