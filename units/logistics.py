from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
import random
from luna_facilities.core.unit import Unit
from luna_facilities.core.snapshot import Snapshot

@dataclass
class LogisticsPipeline(Unit):
    name: str = "LogisticsPipeline"
    shipments: List[Dict[str, Any]] = field(default_factory=list)  # {eta_hours, payload, qty,...}

    def observe(self) -> Snapshot:
        return Snapshot({"shipments": tuple(tuple(sorted(s.items())) for s in self.shipments)})

    def step_exogenous(self, dt: float, rng: random.Random) -> None:
        # decrement ETAs, add random delay noise if desired
        for s in self.shipments:
            s["eta_hours"] = max(0.0, s.get("eta_hours", 0.0) - dt)
