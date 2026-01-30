from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict
import random
from luna_facilities.core.unit import Unit
from luna_facilities.core.snapshot import Snapshot

@dataclass
class PropellantDepot(Unit):
    name: str = "PropellantDepot"

    # depot_id -> prop_name -> mass_kg
    tanks: Dict[str, Dict[str, float]] = field(default_factory=dict)

    transfer_rate_kg_per_step: float = 1000.0
    boiloff_frac_per_day: Dict[str, float] = field(default_factory=lambda: {"LOX": 0.0002, "LH2": 0.0015})
    zero_boiloff_enabled: bool = False

    def observe(self) -> Snapshot:
        return Snapshot({
            "tanks": self.tanks,
            "transfer_rate_kg_per_step": self.transfer_rate_kg_per_step,
            "zero_boiloff_enabled": self.zero_boiloff_enabled,
        })

    def step_exogenous(self, dt: float, rng: random.Random) -> None:
        # dt is in hours unless you choose otherwise; convert to days
        days = dt / 24.0
        if self.zero_boiloff_enabled:
            return
        for depot_id, props in self.tanks.items():
            for prop, mass in list(props.items()):
                frac = self.boiloff_frac_per_day.get(prop, 0.0)
                props[prop] = max(0.0, mass * (1.0 - frac) ** max(0.0, days))

    def add(self, depot_id: str, prop: str, amount_kg: float) -> float:
        self.tanks.setdefault(depot_id, {})
        self.tanks[depot_id][prop] = self.tanks[depot_id].get(prop, 0.0) + max(0.0, amount_kg)
        return max(0.0, amount_kg)

    def transfer(self, depot_id: str, prop: str, amount_kg: float) -> float:
        avail = self.tanks.get(depot_id, {}).get(prop, 0.0)
        moved = min(avail, max(0.0, amount_kg), self.transfer_rate_kg_per_step)
        self.tanks[depot_id][prop] = avail - moved
        return moved
