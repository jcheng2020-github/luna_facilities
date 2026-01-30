from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

@dataclass
class CostModel:
    """
    Converts metrics into scalar cost.
    """
    def total_cost(self, metrics: Dict[str, float], weights: Dict[str, float]) -> float:
        return sum(weights.get(k, 0.0) * metrics.get(k, 0.0) for k in weights.keys())
