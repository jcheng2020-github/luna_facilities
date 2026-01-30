from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict
from luna_facilities.core.unit import Unit
from luna_facilities.core.snapshot import Snapshot

@dataclass
class RiskModel(Unit):
    name: str = "RiskModel"
    constraints: Dict[str, Any] = field(default_factory=dict)
    weights: Dict[str, float] = field(default_factory=lambda: {"health_low": 10.0, "cert_fail": 50.0})

    def observe(self) -> Snapshot:
        return Snapshot({"constraints": self.constraints, "weights": self.weights})

    def risk_score(self, obs: Dict[str, Any]) -> float:
        # lightweight example
        score = 0.0
        return score
