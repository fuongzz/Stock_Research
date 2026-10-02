# Data Model

## Core schemas

### StockFingerprint

`symbol`, `as_of`, `window_start`, `window_end`, feature values, `cluster_id`, regime, sample count, dataset fingerprint.

### Hypothesis

Immutable registration containing statement, target, horizon, population, pre-registration time, and falsification rule.

### Experiment

Experiment ID, hypothesis ID, config, dataset fingerprint, code version, creation time, and results pointer/summary.

### Alpha

Formula, feature set, horizon, train/validation metrics, status, and eventual production eligibility.

### MarketRegime

Point-in-time label, method, regime features, and confidence. Regime models must also be fit chronologically.

### HistoricalAnalogue

Query symbol/date, analogue symbol/date, distance, cluster, and forward outcomes.

## Required supporting tables

- `instrument_master_pit`: symbol identity, listing/delisting dates, sector history, corporate-action links.
- `universe_membership_pit`: membership effective dates, index/sector universe.
- `bars_daily_raw`: immutable vendor payload and ingestion metadata.
- `bars_daily_adjusted`: adjustment method and version.
- `experiment_artifacts`: checksums and storage URIs.
- `data_quality_events`: missing bars, halts, stale prices, symbol changes.

