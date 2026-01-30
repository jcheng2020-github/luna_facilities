from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict
import random
from luna_facilities.core.unit import Unit
from luna_facilities.core.snapshot import Snapshot

@dataclass
class OrbitCatalog(Unit):
    name: str = "OrbitCatalog"
    orbit_state: Dict[str, Dict[str, float]] = field(default_factory=dict)  # asset_id -> state dict
    dv_remaining: Dict[str, float] = field(default_factory=dict)

    def observe(self) -> Snapshot:
        return Snapshot({"orbit_state": self.orbit_state, "dv_remaining": self.dv_remaining})

    def step_exogenous(self, dt: float, rng: random.Random) -> None:
        # placeholder: propagate orbit states
        pass

    def apply_maneuver(self, asset_id: str, dv: float) -> None:
        self.dv_remaining[asset_id] = max(0.0, self.dv_remaining.get(asset_id, 0.0) - max(0.0, dv))
