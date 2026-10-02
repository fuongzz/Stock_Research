from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Any, Dict, List, Optional


@dataclass
class StockFingerprint:
    symbol: str
    as_of: str
    window_start: str
    window_end: str
    feature_values: Dict[str, float]
    cluster_id: Optional[int] = None
    regime: Optional[str] = None
    sample_count: int = 0
    data_fingerprint: str = ""


@dataclass
class Hypothesis:
    hypothesis_id: str
    statement: str
    target: str
    horizon_days: int
    population: str
    pre_registered_at: str
    falsification_rule: str
    status: str = "REGISTERED"


@dataclass
class Experiment:
    experiment_id: str
    name: str
    hypothesis_id: str
    config: Dict[str, Any]
    dataset_fingerprint: str
    code_version: str
    created_at: str
    results: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Alpha:
    alpha_id: str
    name: str
    formula: str
    feature_set: List[str]
    expected_horizon: int
    training_metrics: Dict[str, float]
    validation_metrics: Dict[str, float]
    status: str = "CANDIDATE"


@dataclass
class MarketRegime:
    as_of: str
    label: str
    method: str
    features: Dict[str, float]
    confidence: float


@dataclass
class HistoricalAnalogue:
    query_symbol: str
    query_date: str
    analogue_symbol: str
    analogue_date: str
    distance: float
    forward_returns: Dict[str, float]
    cluster_id: Optional[int] = None


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)

