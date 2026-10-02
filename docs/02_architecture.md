# Architecture

```text
                 +--------------------------+
                 | Data adapters            |
                 | CSV / vendor / database  |
                 +------------+-------------+
                              |
                 +------------v-------------+
                 | Research data contract  |
                 | OHLCV + universe + events|
                 +------------+-------------+
                              |
        +---------------------v----------------------+
        | Feature and window builder                 |
        | returns, volatility, volume, trend, beta  |
        +---------------------+----------------------+
                              |
        +---------------------v----------------------+
        | Experiment engine                         |
        | split -> fit -> predict -> evaluate       |
        +----------+------------------+--------------+
                   |                  |
       +-----------v--------+  +------v---------------+
       | Fingerprint store  |  | Report/audit store    |
       | clusters, regimes  |  | configs, hashes, logs |
       +--------------------+  +-----------------------+

Optional LLM provider -> narrative only; never mutates numeric artifacts.
Separate live layer consumes validated artifacts but does not train on live data.
```

## Boundaries

- `data.py`: validation, normalization, dataset hashing.
- `features.py`: deterministic features and forward labels.
- `clustering.py`: train-time scaler/PCA/cluster model.
- `evaluation.py`: chronological walk-forward evaluation.
- `experiment.py`: orchestration and report writing.
- `providers.py`: optional OpenAI/Claude adapters.

## Planned production services

Object storage for immutable raw snapshots; relational metadata store; feature/artifact registry; scheduler; research notebook/UI; and a read-only serving API for validated fingerprints.

