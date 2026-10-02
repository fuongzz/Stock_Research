# VN Stock Behavioral Research Platform

Research-first multi-agent platform for discovering stock-specific behavioral fingerprints, dynamic stock-window clusters, and validated alpha candidates in Vietnamese equities.

## Design principles

- Python computes every metric, feature, model, split, and backtest result.
- No lookahead: features at date `t` only use observations available at or before `t`; forward returns begin after `t`.
- No survivorship leakage: production ingestion must persist delisted/renamed symbols and point-in-time universe membership.
- Research and live layers are separate. This repository contains the research core and provider interfaces only.
- Every experiment has a config, dataset fingerprint, code version, split definition, and machine-readable report.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m vnstock_research.cli run-exp-001 --output artifacts/exp-001
pytest
```

Core runtime dependencies are `numpy`, `pandas`, and `scikit-learn`. HDBSCAN is optional; EXP-001 falls back to KMeans when it is unavailable or when the configured method is `kmeans`.

## Layout

- `docs/`: product, research, architecture, data model, protocols, agent roles, roadmap.
- `vnstock_research/`: typed schemas, feature engineering, clustering, evaluation, experiment orchestration, provider abstraction.
- `tests/`: deterministic unit and smoke tests.
- `artifacts/`: generated reports; ignored by the intended project setup.

## Real data contract

The first adapter should emit a long-form DataFrame with:

`symbol, date, open, high, low, close, volume, adjusted_close`

Dates must be normalized to exchange sessions, prices must be adjusted consistently for corporate actions, and a point-in-time instrument master must be retained separately from prices.

## LLM/API boundary

No API key is required for EXP-001. `providers.py` defines an interface for optional Claude/OpenAI research narration and hypothesis drafting. Provider output is advisory text only and cannot write metrics or alter experiment results.

