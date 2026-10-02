# Product and Research Vision

## Thesis

Vietnamese equities are heterogeneous. A useful research system should learn *when* a stock behaves like a particular historical family, rather than assume one global predictor applies to every symbol.

The product is a research operating system that converts point-in-time market data into:

1. Stock behavioral fingerprints.
2. Dynamic stock-window clusters.
3. Registered hypotheses and reproducible experiments.
4. A validated alpha library with explicit degradation and invalidation rules.
5. Historical analogues and market-regime context.

## Non-goals

This is not an autonomous trading bot, price oracle, or LLM-based metric engine. No live order placement belongs in the research layer.

## Research questions

- Do stock-window feature vectors form stable behavioral families?
- Are cluster-conditioned forward returns different from the unconditional baseline after costs?
- Which fingerprints persist across market regimes, sectors, and time periods?
- Does a candidate alpha survive walk-forward evaluation, multiple-testing correction, and realistic liquidity constraints?

## Success criteria

An experiment is useful only if it is reproducible, point-in-time valid, economically interpretable, and robust out of sample. Positive in-sample returns alone are not success.

