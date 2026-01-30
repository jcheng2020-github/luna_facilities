from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
import random
from luna_facilities.core.unit import Unit
from luna_facilities.core.snapshot import Snapshot

@dataclass
class DemandModel(Unit):
    name: str = "DemandModel"
    tasks: List[Dict[str, Any]] = field(default_factory=list)  # {id, due_time, priority, payload_kg,...}

    def observe(self) -> Snapshot:
        return Snapshot({"tasks": tuple(tuple(sorted(t.items())) for t in self.tasks)})

    def step_exogenous(self, dt: float, rng: random.Random) -> None:
        # optional: stochastic new demand
        pass
